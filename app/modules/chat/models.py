from datetime import datetime


class Conversation:
    def __init__(self, id=None, title='New Chat', created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            title=data.get('title', 'New Chat'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row['id'],
            title=row['title'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )

    def __eq__(self, other):
        if not isinstance(other, Conversation):
            return False
        return (self.id == other.id
                and self.title == other.title
                and self.created_at == other.created_at
                and self.updated_at == other.updated_at)


class Message:
    def __init__(self, id=None, conversation_id=None, role='user', content='', created_at=None):
        self.id = id
        self.conversation_id = conversation_id
        self.role = role
        self.content = content
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role,
            'content': self.content,
            'created_at': self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            conversation_id=data.get('conversation_id'),
            role=data.get('role', 'user'),
            content=data.get('content', ''),
            created_at=data.get('created_at'),
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row['id'],
            conversation_id=row['conversation_id'],
            role=row['role'],
            content=row['content'],
            created_at=row['created_at'],
        )

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return (self.id == other.id
                and self.conversation_id == other.conversation_id
                and self.role == other.role
                and self.content == other.content
                and self.created_at == other.created_at)
