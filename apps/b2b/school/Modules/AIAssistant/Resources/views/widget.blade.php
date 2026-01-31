{{-- AI Assistant Chatbot Widget --}}
<style>
    .ai-chat-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .ai-chat-button {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .ai-chat-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
    }

    .ai-chat-button svg {
        width: 30px;
        height: 30px;
        fill: white;
    }

    .ai-chat-window {
        position: absolute;
        bottom: 80px;
        right: 0;
        width: 380px;
        height: 500px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        display: none;
        flex-direction: column;
        overflow: hidden;
    }

    .ai-chat-window.active {
        display: flex;
        animation: slideUp 0.3s ease;
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .ai-chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .ai-chat-header h4 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
    }

    .ai-chat-header .close-btn {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 24px;
        line-height: 1;
        opacity: 0.8;
    }

    .ai-chat-header .close-btn:hover {
        opacity: 1;
    }

    .ai-chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        background: #f8f9fa;
    }

    .ai-message {
        margin-bottom: 12px;
        display: flex;
        flex-direction: column;
    }

    .ai-message.user {
        align-items: flex-end;
    }

    .ai-message.bot {
        align-items: flex-start;
    }

    .ai-message .bubble {
        max-width: 85%;
        padding: 12px 16px;
        border-radius: 16px;
        font-size: 14px;
        line-height: 1.5;
    }

    .ai-message.user .bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }

    .ai-message.bot .bubble {
        background: white;
        color: #333;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .ai-chat-input {
        padding: 16px;
        border-top: 1px solid #e9ecef;
        display: flex;
        gap: 10px;
        background: white;
    }

    .ai-chat-input input {
        flex: 1;
        padding: 12px 16px;
        border: 2px solid #e9ecef;
        border-radius: 24px;
        font-size: 14px;
        outline: none;
        transition: border-color 0.3s;
    }

    .ai-chat-input input:focus {
        border-color: #667eea;
    }

    .ai-chat-input button {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.2s;
    }

    .ai-chat-input button:hover {
        transform: scale(1.05);
    }

    .ai-chat-input button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .ai-chat-input button svg {
        width: 20px;
        height: 20px;
        fill: white;
    }

    .ai-typing {
        display: flex;
        gap: 4px;
        padding: 8px 16px;
    }

    .ai-typing span {
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }

    .ai-typing span:nth-child(2) {
        animation-delay: 0.2s;
    }

    .ai-typing span:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-8px);
        }
    }

    .ai-quick-actions {
        padding: 8px 16px;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        background: #f8f9fa;
        border-top: 1px solid #e9ecef;
    }

    .ai-quick-btn {
        padding: 6px 12px;
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 16px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.2s;
    }

    .ai-quick-btn:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }

    /* RTL Support */
    [dir="rtl"] .ai-chat-widget {
        left: 20px;
        right: auto;
    }

    [dir="rtl"] .ai-chat-window {
        left: 0;
        right: auto;
    }

    [dir="rtl"] .ai-message.user .bubble {
        border-bottom-right-radius: 16px;
        border-bottom-left-radius: 4px;
    }

    [dir="rtl"] .ai-message.bot .bubble {
        border-bottom-left-radius: 16px;
        border-bottom-right-radius: 4px;
    }

    /* Mobile responsive */
    @media (max-width: 480px) {
        .ai-chat-window {
            width: calc(100vw - 40px);
            height: calc(100vh - 120px);
            bottom: 70px;
        }
    }
</style>

<div class="ai-chat-widget" id="aiChatWidget">
    <!-- Toggle Button -->
    <button class="ai-chat-button" id="aiChatToggle" title="Assistant IA">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
        </svg>
    </button>

    <!-- Chat Window -->
    <div class="ai-chat-window" id="aiChatWindow">
        <div class="ai-chat-header">
            <h4>{{ setting('application_name') ?? 'IAFactory' }} - Assistant IA</h4>
            <button class="close-btn" id="aiChatClose">&times;</button>
        </div>

        <div class="ai-chat-messages" id="aiChatMessages">
            <div class="ai-message bot">
                <div class="bubble">
                    Bonjour ! Je suis l'assistant virtuel de {{ setting('application_name') ?? "l'école" }}. Comment puis-je vous aider ?
                </div>
            </div>
        </div>

        <div class="ai-quick-actions">
            <button class="ai-quick-btn" data-message="Comment voir les notes ?">Notes</button>
            <button class="ai-quick-btn" data-message="Comment payer les frais ?">Frais</button>
            <button class="ai-quick-btn" data-message="Emploi du temps">Emploi du temps</button>
            <button class="ai-quick-btn" data-message="Contacter un enseignant">Contact</button>
        </div>

        <div class="ai-chat-input">
            <input type="text" id="aiChatInput" placeholder="Posez votre question..." autocomplete="off">
            <button id="aiChatSend" title="Envoyer">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                </svg>
            </button>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const widget = document.getElementById('aiChatWidget');
    const toggleBtn = document.getElementById('aiChatToggle');
    const closeBtn = document.getElementById('aiChatClose');
    const chatWindow = document.getElementById('aiChatWindow');
    const messagesContainer = document.getElementById('aiChatMessages');
    const inputField = document.getElementById('aiChatInput');
    const sendBtn = document.getElementById('aiChatSend');
    const quickBtns = document.querySelectorAll('.ai-quick-btn');

    // Toggle chat window
    toggleBtn.addEventListener('click', () => {
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            inputField.focus();
        }
    });

    closeBtn.addEventListener('click', () => {
        chatWindow.classList.remove('active');
    });

    // Quick action buttons
    quickBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const message = btn.dataset.message;
            inputField.value = message;
            sendMessage();
        });
    });

    // Send message
    function sendMessage() {
        const message = inputField.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, 'user');
        inputField.value = '';
        sendBtn.disabled = true;

        // Show typing indicator
        const typingId = showTyping();

        // Send to API
        fetch('/api/ai/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]')?.content || ''
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            hideTyping(typingId);
            if (data.success) {
                addMessage(data.response, 'bot');
            } else {
                addMessage(data.message || 'Désolé, une erreur est survenue.', 'bot');
            }
        })
        .catch(error => {
            hideTyping(typingId);
            addMessage('Désolé, je ne peux pas répondre pour le moment.', 'bot');
            console.error('AI Chat Error:', error);
        })
        .finally(() => {
            sendBtn.disabled = false;
        });
    }

    // Add message to chat
    function addMessage(text, type) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `ai-message ${type}`;
        msgDiv.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Show typing indicator
    function showTyping() {
        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.id = id;
        typingDiv.className = 'ai-message bot';
        typingDiv.innerHTML = '<div class="ai-typing"><span></span><span></span><span></span></div>';
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return id;
    }

    // Hide typing indicator
    function hideTyping(id) {
        const typingDiv = document.getElementById(id);
        if (typingDiv) typingDiv.remove();
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Send on Enter key
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Send button click
    sendBtn.addEventListener('click', sendMessage);
});
</script>
