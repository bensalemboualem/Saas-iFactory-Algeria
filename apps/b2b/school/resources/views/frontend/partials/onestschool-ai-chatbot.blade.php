{{-- OnestSchool AI Chatbot Widget --}}
<div id="onestschool-ai-chatbot" class="onest-chatbot-widget">
    {{-- Bouton flottant avec animation --}}
    <div id="chatbot-toggle" class="chatbot-toggle">
        <div class="chatbot-icon">
            <svg viewBox="0 0 24 24" width="24" height="24">
                <path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,6A4,4 0 0,1 16,10V11A2,2 0 0,1 14,13H13V16H11V13H10A2,2 0 0,1 8,11V10A4,4 0 0,1 12,6M12,8A2,2 0 0,0 10,10V11H14V10A2,2 0 0,0 12,8Z"/>
            </svg>
        </div>
        <div class="chatbot-badge">
            <span>IA</span>
        </div>
        <div class="pulse-ring"></div>
    </div>

    {{-- Fenêtre de chat --}}
    <div id="chatbot-window" class="chatbot-window">
        {{-- En-tête OnestSchool --}}
        <div class="chatbot-header">
            <div class="header-content">
                <div class="chatbot-avatar">
                    <svg viewBox="0 0 24 24" width="32" height="32">
                        <path fill="#4CAF50" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,6A4,4 0 0,1 16,10V11A2,2 0 0,1 14,13H13V16H11V13H10A2,2 0 0,1 8,11V10A4,4 0 0,1 12,6M12,8A2,2 0 0,0 10,10V11H14V10A2,2 0 0,0 12,8Z"/>
                    </svg>
                </div>
                <div class="header-info">
                    <h4>Assistant IA OnestSchool</h4>
                    <p class="online-status">🟢 En ligne • Assistance 24/7</p>
                </div>
            </div>
            <button id="chatbot-close" class="close-btn">&times;</button>
        </div>

        {{-- Zone des messages --}}
        <div id="chatbot-messages" class="chatbot-messages">
            {{-- Message de bienvenue --}}
            <div class="message bot-message">
                <div class="message-avatar">
                    <svg viewBox="0 0 24 24" width="20" height="20">
                        <path fill="#4CAF50" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,6A4,4 0 0,1 16,10V11A2,2 0 0,1 14,13H13V16H11V13H10A2,2 0 0,1 8,11V10A4,4 0 0,1 12,6M12,8A2,2 0 0,0 10,10V11H14V10A2,2 0 0,0 12,8Z"/>
                    </svg>
                </div>
                <div class="message-content">
                    <div class="message-text">
                        🎓 <strong>Bienvenue sur OnestSchool !</strong><br>
                        Je suis votre assistant IA personnalisé. Je peux vous aider avec :
                        <ul style="margin: 8px 0; padding-left: 20px;">
                            <li>Navigation dans la plateforme</li>
                            <li>Gestion académique</li>
                            <li>Support technique</li>
                            <li>Questions générales</li>
                        </ul>
                        Comment puis-je vous assister aujourd'hui ?
                    </div>
                    <div class="message-time">Maintenant</div>
                </div>
            </div>
        </div>

        {{-- Actions rapides contextuelles --}}
        <div id="quick-actions" class="quick-actions">
            <div class="actions-header">
                <span>🚀 Actions rapides</span>
            </div>
            <div class="actions-grid" id="actions-buttons">
                {{-- Chargées dynamiquement selon le profil utilisateur --}}
            </div>
        </div>

        {{-- Zone de saisie --}}
        <div class="chatbot-input">
            <div class="input-container">
                <input type="text" id="chatbot-input" placeholder="Posez votre question..." maxlength="500">
                <button id="chatbot-send" class="send-btn">
                    <svg viewBox="0 0 24 24" width="20" height="20">
                        <path fill="currentColor" d="M2,21L23,12L2,3V10L17,12L2,14V21Z"/>
                    </svg>
                </button>
            </div>
            <div class="typing-indicator" id="typing-indicator" style="display: none;">
                <span>Assistant IA est en train d'écrire</span>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    </div>
</div>

{{-- Styles CSS OnestSchool --}}
<style>
.onest-chatbot-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 10000;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Bouton flottant */
.chatbot-toggle {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, #4CAF50, #45a049);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.chatbot-toggle:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(76, 175, 80, 0.4);
}

.chatbot-icon {
    color: white;
    transition: transform 0.3s ease;
}

.chatbot-toggle:hover .chatbot-icon {
    transform: scale(1.1);
}

.chatbot-badge {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #FF5722;
    color: white;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: bold;
    animation: bounce 2s infinite;
}

.pulse-ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border: 3px solid rgba(76, 175, 80, 0.6);
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    100% { transform: scale(1.4); opacity: 0; }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

/* Fenêtre de chat */
.chatbot-window {
    position: absolute;
    bottom: 80px;
    right: 0;
    width: 380px;
    height: 600px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    display: none;
    flex-direction: column;
    overflow: hidden;
    animation: slideInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* En-tête */
.chatbot-header {
    background: linear-gradient(135deg, #4CAF50, #45a049);
    color: white;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-content {
    display: flex;
    align-items: center;
    gap: 12px;
}

.chatbot-avatar {
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.header-info h4 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
}

.online-status {
    margin: 2px 0 0 0;
    font-size: 12px;
    opacity: 0.9;
}

.close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
    padding: 5px;
    border-radius: 50%;
    transition: background 0.2s;
}

.close-btn:hover {
    background: rgba(255, 255, 255, 0.2);
}

/* Messages */
.chatbot-messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    max-height: 350px;
}

.message {
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
    animation: messageSlide 0.3s ease-out;
}

@keyframes messageSlide {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.bot-message .message-avatar {
    background: #E8F5E8;
}

.user-message {
    flex-direction: row-reverse;
}

.user-message .message-avatar {
    background: #2196F3;
    color: white;
}

.message-content {
    flex: 1;
    max-width: 280px;
}

.message-text {
    background: #f5f5f5;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 14px;
    line-height: 1.4;
    word-wrap: break-word;
}

.bot-message .message-text {
    background: #E8F5E8;
    border-bottom-left-radius: 6px;
}

.user-message .message-text {
    background: #2196F3;
    color: white;
    border-bottom-right-radius: 6px;
}

.message-time {
    font-size: 11px;
    color: #666;
    margin-top: 4px;
    text-align: right;
}

.user-message .message-time {
    text-align: left;
}

/* Actions rapides */
.quick-actions {
    border-top: 1px solid #eee;
    padding: 15px 20px;
    background: #fafafa;
}

.actions-header {
    font-size: 12px;
    font-weight: 600;
    color: #666;
    margin-bottom: 10px;
}

.actions-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}

.action-btn {
    padding: 8px 12px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 20px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
}

.action-btn:hover {
    background: #4CAF50;
    color: white;
    border-color: #4CAF50;
}

/* Zone de saisie */
.chatbot-input {
    border-top: 1px solid #eee;
    padding: 15px 20px;
}

.input-container {
    display: flex;
    gap: 10px;
    align-items: center;
}

#chatbot-input {
    flex: 1;
    padding: 12px 16px;
    border: 1px solid #ddd;
    border-radius: 25px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
}

#chatbot-input:focus {
    border-color: #4CAF50;
}

.send-btn {
    width: 45px;
    height: 45px;
    background: #4CAF50;
    border: none;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}

.send-btn:hover {
    background: #45a049;
}

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #666;
    margin-top: 8px;
}

.typing-dots {
    display: flex;
    gap: 3px;
}

.typing-dots span {
    width: 6px;
    height: 6px;
    background: #4CAF50;
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
    0%, 80%, 100% {
        transform: scale(0);
        opacity: 0.5;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}

/* Responsive */
@media (max-width: 480px) {
    .chatbot-window {
        width: calc(100vw - 40px);
        height: calc(100vh - 100px);
        bottom: 80px;
        right: 20px;
    }
    
    .actions-grid {
        grid-template-columns: 1fr;
    }
}

/* Animation smooth pour l'ouverture */
.chatbot-window.show {
    display: flex;
    animation: slideInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.chatbot-window.hide {
    animation: slideOutDown 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideOutDown {
    from {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
    to {
        opacity: 0;
        transform: translateY(30px) scale(0.95);
    }
}
</style>

{{-- JavaScript OnestSchool IA --}}
<script>
class OnestSchoolAI {
    constructor() {
        this.isOpen = false;
        this.isTyping = false;
        this.userType = 'visitor';
        
        this.init();
        this.loadQuickActions();
        this.bindEvents();
    }
    
    init() {
        // Configuration CSRF pour Laravel
        const token = document.querySelector('meta[name="csrf-token"]');
        if (token) {
            window.axios.defaults.headers.common['X-CSRF-TOKEN'] = token.getAttribute('content');
        }
        
        // Charger les données contextuelles
        this.loadContextData();
    }
    
    bindEvents() {
        const toggle = document.getElementById('chatbot-toggle');
        const close = document.getElementById('chatbot-close');
        const input = document.getElementById('chatbot-input');
        const send = document.getElementById('chatbot-send');
        
        toggle.addEventListener('click', () => this.toggleChat());
        close.addEventListener('click', () => this.closeChat());
        send.addEventListener('click', () => this.sendMessage());
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize sur mobile
        window.addEventListener('resize', () => this.adjustForMobile());
    }
    
    async loadContextData() {
        try {
            const response = await fetch('/chatbot/context', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.userType = data.userType || 'visitor';
                this.updateWelcomeMessage(data);
                this.loadQuickActions();
            }
        } catch (error) {
            console.log('Context loading failed:', error);
        }
    }
    
    updateWelcomeMessage(data) {
        const welcomeText = document.querySelector('.bot-message .message-text');
        if (welcomeText && data.user && data.user !== 'Visiteur') {
            welcomeText.innerHTML = `
                🎓 <strong>Bonjour ${data.user} !</strong><br>
                Bienvenue sur votre espace OnestSchool. Je suis votre assistant IA personnalisé.
                <br><br>
                En tant que <strong>${this.getUserTypeLabel(data.userType)}</strong>, je peux vous aider avec toutes vos questions sur la plateforme.
                <br><br>
                Comment puis-je vous assister aujourd'hui ?
            `;
        }
    }
    
    getUserTypeLabel(type) {
        const labels = {
            'admin': 'Administrateur',
            'teacher': 'Enseignant',
            'student': 'Étudiant',
            'parent': 'Parent',
            'visitor': 'Visiteur'
        };
        return labels[type] || 'Utilisateur';
    }
    
    async loadQuickActions() {
        try {
            const response = await fetch('/chatbot/context');
            if (response.ok) {
                const data = await response.json();
                this.renderQuickActions(data.suggestions || []);
            }
        } catch (error) {
            console.log('Quick actions failed:', error);
        }
    }
    
    renderQuickActions(suggestions) {
        const container = document.getElementById('actions-buttons');
        container.innerHTML = '';
        
        suggestions.slice(0, 4).forEach(suggestion => {
            const btn = document.createElement('button');
            btn.className = 'action-btn';
            btn.textContent = suggestion;
            btn.addEventListener('click', () => this.sendQuickAction(suggestion));
            container.appendChild(btn);
        });
    }
    
    toggleChat() {
        const window = document.getElementById('chatbot-window');
        
        if (this.isOpen) {
            this.closeChat();
        } else {
            window.style.display = 'flex';
            window.classList.add('show');
            this.isOpen = true;
            
            // Focus sur l'input
            setTimeout(() => {
                document.getElementById('chatbot-input').focus();
            }, 300);
        }
    }
    
    closeChat() {
        const window = document.getElementById('chatbot-window');
        window.classList.remove('show');
        window.classList.add('hide');
        
        setTimeout(() => {
            window.style.display = 'none';
            window.classList.remove('hide');
            this.isOpen = false;
        }, 300);
    }
    
    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Ajouter le message utilisateur
        this.addMessage(message, 'user');
        input.value = '';
        
        // Afficher l'indicateur de frappe
        this.showTyping();
        
        try {
            const response = await fetch('/chatbot/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content'),
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            setTimeout(() => {
                this.hideTyping();
                if (data.success) {
                    this.addMessage(data.response, 'bot');
                } else {
                    this.addMessage('❌ Désolé, une erreur s\'est produite. Veuillez réessayer.', 'bot');
                }
            }, 1000);
            
        } catch (error) {
            console.error('Chat error:', error);
            setTimeout(() => {
                this.hideTyping();
                this.addMessage('🔌 Problème de connexion. Vérifiez votre réseau.', 'bot');
            }, 1000);
        }
    }
    
    sendQuickAction(action) {
        this.addMessage(action, 'user');
        
        setTimeout(() => {
            this.sendMessage();
        }, 100);
        
        document.getElementById('chatbot-input').value = action;
    }
    
    addMessage(text, type) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        const time = new Date().toLocaleTimeString('fr-FR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        messageDiv.className = `message ${type}-message`;
        messageDiv.innerHTML = `
            <div class="message-avatar">
                ${type === 'bot' ? 
                    '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="#4CAF50" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,6A4,4 0 0,1 16,10V11A2,2 0 0,1 14,13H13V16H11V13H10A2,2 0 0,1 8,11V10A4,4 0 0,1 12,6M12,8A2,2 0 0,0 10,10V11H14V10A2,2 0 0,0 12,8Z"/></svg>' :
                    '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,6A4,4 0 0,1 16,10A4,4 0 0,1 12,14A4,4 0 0,1 8,10A4,4 0 0,1 12,6Z"/></svg>'
                }
            </div>
            <div class="message-content">
                <div class="message-text">${this.formatMessage(text)}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    formatMessage(text) {
        // Support du Markdown basique
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
            .replace(/\n/g, '<br>');
    }
    
    showTyping() {
        this.isTyping = true;
        document.getElementById('typing-indicator').style.display = 'flex';
    }
    
    hideTyping() {
        this.isTyping = false;
        document.getElementById('typing-indicator').style.display = 'none';
    }
    
    adjustForMobile() {
        if (window.innerWidth <= 480 && this.isOpen) {
            const window = document.getElementById('chatbot-window');
            window.style.width = `${window.innerWidth - 40}px`;
            window.style.height = `${window.innerHeight - 100}px`;
        }
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    window.onestSchoolAI = new OnestSchoolAI();
});

// Debug pour développement
console.log('🎓 OnestSchool AI Chatbot initialisé');
</script>