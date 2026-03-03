from flask import render_template, request, jsonify, current_app
from . import chat_bp
from .service import ChatService


def get_service():
    return ChatService(current_app._get_current_object())


@chat_bp.route('/')
def chat_page():
    modules = current_app.config.get('REGISTERED_MODULES', [])
    return render_template('chat/chat.html', modules=modules, active_module='chat')


@chat_bp.route('/api/conversations', methods=['GET'])
def list_conversations():
    service = get_service()
    conversations = service.get_conversations()
    return jsonify([c.to_dict() for c in conversations])


@chat_bp.route('/api/conversations', methods=['POST'])
def create_conversation():
    service = get_service()
    conv = service.create_conversation()
    return jsonify(conv.to_dict()), 201


@chat_bp.route('/api/conversations/<int:conv_id>', methods=['DELETE'])
def delete_conversation(conv_id):
    service = get_service()
    conv = service.get_conversation(conv_id)
    if not conv:
        return jsonify({'error': 'Conversation not found'}), 404
    service.delete_conversation(conv_id)
    return jsonify({'success': True})


@chat_bp.route('/api/conversations/<int:conv_id>/messages', methods=['GET'])
def list_messages(conv_id):
    service = get_service()
    conv = service.get_conversation(conv_id)
    if not conv:
        return jsonify({'error': 'Conversation not found'}), 404
    messages = service.get_messages(conv_id)
    return jsonify([m.to_dict() for m in messages])


@chat_bp.route('/api/conversations/<int:conv_id>/messages', methods=['POST'])
def send_message(conv_id):
    service = get_service()
    conv = service.get_conversation(conv_id)
    if not conv:
        return jsonify({'error': 'Conversation not found'}), 404

    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({'error': 'Message content is required'}), 400

    content = data['content']
    try:
        user_msg, assistant_msg = service.send_message(conv_id, content)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({
        'user_message': user_msg.to_dict(),
        'assistant_message': assistant_msg.to_dict(),
    })
