const API = '/chat/api';
let currentConvId = null;
let isLoading = false;

// DOM Elements
const convList = document.getElementById('convList');
const chatMessages = document.getElementById('chatMessages');
const chatEmpty = document.getElementById('chatEmpty');
const chatInput = document.getElementById('chatInput');
const btnSend = document.getElementById('btnSend');
const btnNewChat = document.getElementById('btnNewChat');

// === API Calls ===

async function fetchConversations() {
    const res = await fetch(`${API}/conversations`);
    return res.json();
}

async function createConversation() {
    const res = await fetch(`${API}/conversations`, { method: 'POST' });
    return res.json();
}

async function deleteConversation(id) {
    await fetch(`${API}/conversations/${id}`, { method: 'DELETE' });
}

async function fetchMessages(convId) {
    const res = await fetch(`${API}/conversations/${convId}/messages`);
    return res.json();
}

async function sendMessage(convId, content) {
    const res = await fetch(`${API}/conversations/${convId}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
    });
    return res.json();
}

// === Rendering ===

function renderConversations(conversations) {
    convList.innerHTML = '';
    conversations.forEach(conv => {
        const li = document.createElement('li');
        li.className = `conv-item${conv.id === currentConvId ? ' active' : ''}`;
        li.innerHTML = `
            <span class="conv-item-title">${escapeHtml(conv.title)}</span>
            <button class="conv-item-delete" title="Delete">✕</button>
        `;
        li.querySelector('.conv-item-title').addEventListener('click', () => selectConversation(conv.id));
        li.querySelector('.conv-item-delete').addEventListener('click', (e) => {
            e.stopPropagation();
            handleDelete(conv.id);
        });
        convList.appendChild(li);
    });
}

function renderMessages(messages) {
    // Remove empty state
    if (chatEmpty) chatEmpty.style.display = 'none';

    // Clear existing messages
    chatMessages.querySelectorAll('.message').forEach(el => el.remove());

    if (messages.length === 0 && chatEmpty) {
        chatEmpty.style.display = 'flex';
        return;
    }

    messages.forEach(msg => appendMessage(msg.role, msg.content));
    scrollToBottom();
}

function appendMessage(role, content) {
    if (chatEmpty) chatEmpty.style.display = 'none';

    const div = document.createElement('div');
    div.className = `message ${role}`;

    const avatar = role === 'user' ? '👤' : '🤖';
    div.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-bubble">${escapeHtml(content)}</div>
    `;
    chatMessages.appendChild(div);
    scrollToBottom();
}

function showLoading() {
    const div = document.createElement('div');
    div.className = 'message assistant message-loading';
    div.id = 'loadingIndicator';
    div.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-bubble">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    `;
    chatMessages.appendChild(div);
    scrollToBottom();
}

function hideLoading() {
    const el = document.getElementById('loadingIndicator');
    if (el) el.remove();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// === Event Handlers ===

async function selectConversation(id) {
    currentConvId = id;
    const conversations = await fetchConversations();
    renderConversations(conversations);
    const messages = await fetchMessages(id);
    renderMessages(messages);
    chatInput.focus();
}

async function handleNewChat() {
    const conv = await createConversation();
    currentConvId = conv.id;
    const conversations = await fetchConversations();
    renderConversations(conversations);
    renderMessages([]);
    chatInput.focus();
}

async function handleDelete(id) {
    await deleteConversation(id);
    if (currentConvId === id) {
        currentConvId = null;
        renderMessages([]);
        if (chatEmpty) chatEmpty.style.display = 'flex';
    }
    const conversations = await fetchConversations();
    renderConversations(conversations);
}

async function handleSend() {
    const content = chatInput.value.trim();
    if (!content || isLoading || !currentConvId) return;

    isLoading = true;
    btnSend.disabled = true;
    chatInput.value = '';
    autoResize();

    appendMessage('user', content);
    showLoading();

    try {
        const result = await sendMessage(currentConvId, content);
        console.log('[DEBUG] API response:', result);
        console.log('[DEBUG] Assistant message:', result.assistant_message);
        hideLoading();
        appendMessage('assistant', result.assistant_message.content);

        // Refresh conversation list to update title
        const conversations = await fetchConversations();
        renderConversations(conversations);
    } catch (err) {
        console.error('[DEBUG] Error:', err);
        hideLoading();
        appendMessage('assistant', '⚠️ 오류가 발생했습니다. 다시 시도해주세요.');
    } finally {
        isLoading = false;
        btnSend.disabled = false;
        chatInput.focus();
    }
}

function autoResize() {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
}

// === Event Listeners ===

btnNewChat.addEventListener('click', handleNewChat);
btnSend.addEventListener('click', handleSend);

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

chatInput.addEventListener('input', autoResize);

// === Init ===

(async function init() {
    const conversations = await fetchConversations();
    renderConversations(conversations);
    if (conversations.length > 0) {
        await selectConversation(conversations[0].id);
    }
})();
