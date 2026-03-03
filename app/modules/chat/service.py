import requests
from app.models.base import get_db
from app.modules.chat.models import Conversation, Message


class ChatService:
    def __init__(self, app):
        self.app = app

    def create_conversation(self, title='New Chat'):
        conn = get_db(self.app)
        try:
            cursor = conn.execute(
                "INSERT INTO conversations (title) VALUES (?)",
                (title,)
            )
            conn.commit()
            row = conn.execute(
                "SELECT * FROM conversations WHERE id = ?",
                (cursor.lastrowid,)
            ).fetchone()
            return Conversation.from_row(row)
        finally:
            conn.close()

    def get_conversations(self):
        conn = get_db(self.app)
        try:
            rows = conn.execute(
                "SELECT * FROM conversations ORDER BY updated_at DESC"
            ).fetchall()
            return [Conversation.from_row(r) for r in rows]
        finally:
            conn.close()

    def get_conversation(self, conversation_id):
        conn = get_db(self.app)
        try:
            row = conn.execute(
                "SELECT * FROM conversations WHERE id = ?",
                (conversation_id,)
            ).fetchone()
            return Conversation.from_row(row) if row else None
        finally:
            conn.close()

    def delete_conversation(self, conversation_id):
        conn = get_db(self.app)
        try:
            conn.execute(
                "DELETE FROM conversations WHERE id = ?",
                (conversation_id,)
            )
            conn.commit()
            return True
        finally:
            conn.close()

    def get_messages(self, conversation_id):
        conn = get_db(self.app)
        try:
            rows = conn.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
                (conversation_id,)
            ).fetchall()
            return [Message.from_row(r) for r in rows]
        finally:
            conn.close()

    def add_message(self, conversation_id, role, content):
        """Add a message to a conversation and return it."""
        conn = get_db(self.app)
        try:
            cursor = conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, role, content)
            )
            conn.execute(
                "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (conversation_id,)
            )
            conn.commit()
            row = conn.execute(
                "SELECT * FROM messages WHERE id = ?",
                (cursor.lastrowid,)
            ).fetchone()
            return Message.from_row(row)
        finally:
            conn.close()

    def send_message(self, conversation_id, content):
        """Validate, save user message, call n8n webhook, save AI response."""
        content = content.strip() if content else ''
        if not content:
            raise ValueError("Message content cannot be empty")

        # Save user message
        user_msg = self.add_message(conversation_id, 'user', content)

        # Update conversation title from first message
        conv = self.get_conversation(conversation_id)
        if conv and conv.title == 'New Chat':
            title = content[:50] + ('...' if len(content) > 50 else '')
            conn = get_db(self.app)
            try:
                conn.execute(
                    "UPDATE conversations SET title = ? WHERE id = ?",
                    (title, conversation_id)
                )
                conn.commit()
            finally:
                conn.close()

        # Call n8n webhook
        try:
            ai_response = self._call_n8n_webhook(content, conversation_id)
        except Exception as e:
            error_msg = self.add_message(
                conversation_id, 'assistant',
                f"⚠️ 오류가 발생했습니다: {str(e)}"
            )
            return user_msg, error_msg

        # Save AI response
        assistant_msg = self.add_message(conversation_id, 'assistant', ai_response)
        return user_msg, assistant_msg

    def _call_n8n_webhook(self, content, conversation_id):
        """Call n8n webhook with message and conversation context."""
        webhook_url = self.app.config.get('N8N_WEBHOOK_URL', '')
        if not webhook_url:
            raise ConnectionError("N8N_WEBHOOK_URL이 설정되지 않았습니다. .env 파일을 확인해주세요.")

        timeout = self.app.config.get('N8N_TIMEOUT', 30)

        # Build context from conversation history
        messages = self.get_messages(conversation_id)
        context = [m.to_dict() for m in messages]

        payload = {
            'message': content,
            'conversation_id': conversation_id,
            'context': context,
        }

        try:
            response = requests.post(
                webhook_url,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise TimeoutError("응답 시간이 초과되었습니다")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("서버에 연결할 수 없습니다")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"요청 처리 중 오류가 발생했습니다: {e.response.status_code}")

        # Parse response - try common formats
        try:
            data = response.json()
            if isinstance(data, str):
                return data
            if isinstance(data, dict):
                return data.get('output', data.get('response', data.get('text', str(data))))
            return str(data)
        except ValueError:
            return response.text
