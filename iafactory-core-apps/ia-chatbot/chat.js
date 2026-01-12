/**
 * IAFactory Chatbot - API Integration
 * Connects to backend API for AI chat
 */

// Dynamic API URL detection
const getApiUrl = () => (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:8000'
    : window.location.origin;

class IAFactoryChatbot {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || getApiUrl();
        this.language = options.language || 'fr';
        this.provider = options.provider || 'anthropic';
        this.conversationHistory = [];
        this.isStreaming = false;

        this.init();
    }

    init() {
        this.chatContainer = document.getElementById('chat-container');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.providerSelect = document.getElementById('provider-select');

        if (this.sendButton) {
            this.sendButton.addEventListener('click', () => this.sendMessage());
        }

        if (this.messageInput) {
            this.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }

        if (this.providerSelect) {
            this.providerSelect.addEventListener('change', (e) => {
                this.provider = e.target.value;
            });
        }
    }

    async sendMessage() {
        const message = this.messageInput?.value?.trim();
        if (!message || this.isStreaming) return;

        this.addMessage('user', message);
        this.messageInput.value = '';
        this.isStreaming = true;
        this.sendButton.disabled = true;

        this.conversationHistory.push({ role: 'user', content: message });

        try {
            const assistantDiv = this.addMessage('assistant', '');
            const response = await this.callChatAPI(message);
            assistantDiv.querySelector('.message-content').textContent = response;
            this.conversationHistory.push({ role: 'assistant', content: response });
        } catch (error) {
            console.error('Chat error:', error);
            this.addMessage('system', 'Erreur: ' + error.message);
        } finally {
            this.isStreaming = false;
            this.sendButton.disabled = false;
        }
    }

    async callChatAPI(message) {
        const response = await fetch(this.apiUrl + '/api/agent-chat/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                conversation_history: this.conversationHistory.slice(-10),
                language: this.language,
                provider: this.provider
            })
        });

        if (!response.ok) {
            throw new Error('API error: ' + response.status);
        }

        const data = await response.json();
        return data.response || data.message || 'No response';
    }

    addMessage(role, content) {
        if (!this.chatContainer) return null;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message ' + role + '-message';

        const roleLabels = {
            user: { fr: 'Vous', ar: 'انت', en: 'You' },
            assistant: { fr: 'Assistant', ar: 'المساعد', en: 'Assistant' },
            system: { fr: 'Systeme', ar: 'النظام', en: 'System' }
        };

        const label = roleLabels[role]?.[this.language] || role;

        messageDiv.innerHTML = '<div class="message-header"><span class="message-role">' + label + '</span><span class="message-time">' + new Date().toLocaleTimeString() + '</span></div><div class="message-content">' + (content || '<span class="typing">...</span>') + '</div>';

        this.chatContainer.appendChild(messageDiv);
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;

        return messageDiv;
    }

    clearHistory() {
        this.conversationHistory = [];
        if (this.chatContainer) {
            this.chatContainer.innerHTML = '';
        }
    }

    setLanguage(lang) {
        this.language = lang;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new IAFactoryChatbot({
        apiUrl: window.API_URL || getApiUrl(),
        language: document.documentElement.lang || 'fr'
    });
});
