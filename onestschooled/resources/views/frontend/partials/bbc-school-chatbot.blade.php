{{-- BBC School Algeria Chatbot Widget --}}
<div id="bbc-school-chatbot" class="bbc-chatbot-widget">
    {{-- Bouton flottant BBC School --}}
    <div id="chatbot-toggle" class="chatbot-toggle">
        <div class="chatbot-icon">
            <svg viewBox="0 0 24 24" width="26" height="26">
                <path fill="currentColor" d="M12,3L1,9L12,15L21,12V17H23V10M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/>
            </svg>
        </div>
        <div class="chatbot-badge">
            <span>BBC</span>
        </div>
        <div class="pulse-ring"></div>
    </div>

    {{-- Fenêtre de chat BBC School --}}
    <div id="chatbot-window" class="chatbot-window">
        {{-- En-tête BBC School Algeria --}}
        <div class="chatbot-header">
            <div class="header-content">
                <div class="chatbot-avatar">
                    <svg viewBox="0 0 24 24" width="32" height="32">
                        <path fill="#2196F3" d="M12,3L1,9L12,15L21,12V17H23V10M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/>
                    </svg>
                </div>
                <div class="header-info">
                    <h4>BBC School Algeria</h4>
                    <p class="online-status">🇩🇿 Assistant IA Personnalisé</p>
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
                        <path fill="#2196F3" d="M12,3L1,9L12,15L21,12V17H23V10M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/>
                    </svg>
                </div>
                <div class="message-content">
                    <div class="message-text">
                        🇩🇿 <strong>Bienvenue à BBC School Algeria !</strong><br>
                        Je suis votre assistant IA personnalisé. Je connais votre profil et vos cours.
                        <ul style="margin: 8px 0; padding-left: 20px;">
                            <li><strong>MES COURS</strong> : Votre programme personnel</li>
                            <li><strong>MES NOTES</strong> : Vos résultats individuels</li>
                            <li><strong>MON PLANNING</strong> : Votre emploi du temps</li>
                            <li><strong>SUPPORT</strong> : Aide personnalisée</li>
                        </ul>
                        Comment puis-je vous aider aujourd'hui ?
                    </div>
                    <div class="message-time">Maintenant</div>
                </div>
            </div>
        </div>

        {{-- Actions rapides personnalisées --}}
        <div id="quick-actions" class="quick-actions">
            <div class="actions-header">
                <span>⚡ Actions Personnalisées</span>
                <small id="user-profile-info" style="color: #666;"></small>
            </div>
            <div class="actions-grid" id="actions-buttons">
                {{-- Chargées dynamiquement selon le profil utilisateur connecté --}}
                <button class="action-btn" onclick="sendQuickMessage('mes cours')">📚 MES Cours</button>
                <button class="action-btn" onclick="sendQuickMessage('mes notes')">📊 MES Notes</button>
                <button class="action-btn" onclick="sendQuickMessage('mon planning')">📅 MON Planning</button>
                <button class="action-btn" onclick="sendQuickMessage('aide')">❓ Support</button>
            </div>
        </div>

        {{-- Zone de saisie --}}
        <div class="chatbot-input">
            <div class="input-container">
                <input type="text" id="chatbot-input" placeholder="Posez votre question personnalisée..." maxlength="500">
                <button id="chatbot-send" class="send-btn">
                    <svg viewBox="0 0 24 24" width="20" height="20">
                        <path fill="currentColor" d="M2,21L23,12L2,3V10L17,12L2,14V21Z"/>
                    </svg>
                </button>
            </div>
            <div class="typing-indicator" id="typing-indicator" style="display: none;">
                <span>Assistant BBC School répond...</span>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    </div>
</div>

{{-- Styles CSS BBC School --}}
<style>
.bbc-chatbot-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 10000;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Bouton flottant BBC School */
.chatbot-toggle {
    width: 75px;
    height: 75px;
    background: linear-gradient(135deg, #2196F3, #1976D2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(33, 150, 243, 0.4);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.chatbot-toggle:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 40px rgba(33, 150, 243, 0.5);
}

.chatbot-icon {
    color: white;
    transition: transform 0.3s ease;
}

.chatbot-toggle:hover .chatbot-icon {
    transform: scale(1.15);
}

.chatbot-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background: #FF5722;
    color: white;
    border-radius: 15px;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: bold;
    animation: bounce 2s infinite;
}

.pulse-ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border: 3px solid rgba(33, 150, 243, 0.6);
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

/* Fenêtre de chat BBC School */
.chatbot-window {
    position: absolute;
    bottom: 85px;
    right: 0;
    width: 400px;
    height: 650px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 25px 70px rgba(0, 0, 0, 0.2);
    display: none;
    flex-direction: column;
    overflow: hidden;
    animation: slideInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid #2196F3;
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

/* En-tête BBC School */
.chatbot-header {
    background: linear-gradient(135deg, #2196F3, #1976D2);
    color: white;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-content {
    display: flex;
    align-items: center;
    gap: 15px;
}

.chatbot-avatar {
    width: 45px;
    height: 45px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.header-info h4 {
    margin: 0;
    font-size: 17px;
    font-weight: 700;
}

.online-status {
    margin: 3px 0 0 0;
    font-size: 12px;
    opacity: 0.9;
}

.close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
    padding: 8px;
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
    max-height: 380px;
}

.message {
    display: flex;
    gap: 12px;
    margin-bottom: 18px;
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
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.bot-message .message-avatar {
    background: #E3F2FD;
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
    max-width: 300px;
}

.message-text {
    background: #f8f9fa;
    padding: 14px 18px;
    border-radius: 20px;
    font-size: 14px;
    line-height: 1.5;
    word-wrap: break-word;
}

.bot-message .message-text {
    background: #E3F2FD;
    border-bottom-left-radius: 8px;
}

.user-message .message-text {
    background: #2196F3;
    color: white;
    border-bottom-right-radius: 8px;
}

.message-time {
    font-size: 11px;
    color: #777;
    margin-top: 5px;
    text-align: right;
}

.user-message .message-time {
    text-align: left;
    color: #ccc;
}

/* Actions rapides BBC School */
.quick-actions {
    border-top: 1px solid #e0e0e0;
    padding: 18px 20px;
    background: #fafbfc;
}

.actions-header {
    font-size: 13px;
    font-weight: 600;
    color: #555;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.actions-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

.action-btn {
    padding: 10px 14px;
    background: white;
    border: 2px solid #e0e0e0;
    border-radius: 25px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    text-align: center;
}

.action-btn:hover {
    background: #2196F3;
    color: white;
    border-color: #2196F3;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

/* Zone de saisie */
.chatbot-input {
    border-top: 1px solid #e0e0e0;
    padding: 18px 20px;
    background: white;
}

.input-container {
    display: flex;
    gap: 12px;
    align-items: center;
}

#chatbot-input {
    flex: 1;
    padding: 14px 18px;
    border: 2px solid #e0e0e0;
    border-radius: 25px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.3s;
}

#chatbot-input:focus {
    border-color: #2196F3;
    box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
}

.send-btn {
    width: 48px;
    height: 48px;
    background: #2196F3;
    border: none;
    border-radius: 50%;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
}

.send-btn:hover {
    background: #1976D2;
    transform: scale(1.05);
}

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    color: #666;
    margin-top: 10px;
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dots span {
    width: 7px;
    height: 7px;
    background: #2196F3;
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
        height: calc(100vh - 120px);
        bottom: 85px;
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

/* Indicateur utilisateur connecté */
.user-connected {
    background: #4CAF50 !important;
}

.user-connected .pulse-ring {
    border-color: rgba(76, 175, 80, 0.6) !important;
}
</style>

{{-- JavaScript BBC School IA --}}
<script>
class BBCSchoolChatbot {
    constructor() {
        this.isOpen = false;
        this.isTyping = false;
        this.userProfile = null;
        this.apiEndpoint = '/chatbot/chat';
        
        this.init();
        this.bindEvents();
    }
    
    async init() {
        // Configuration CSRF pour Laravel
        const token = document.querySelector('meta[name="csrf-token"]');
        if (token) {
            this.csrfToken = token.getAttribute('content');
        }
        
        // Charger le profil utilisateur
        await this.loadUserProfile();
        this.updateUIForUser();
    }
    
    async loadUserProfile() {
        try {
            const response = await fetch('/chatbot/context', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            });
            
            if (response.ok) {
                this.userProfile = await response.json();
                console.log('👤 Profil utilisateur BBC School chargé:', this.userProfile);
            }
        } catch (error) {
            console.log('⚠️ Chargement profil échoué:', error);
            this.userProfile = { userType: 'visitor', user: 'Visiteur' };
        }
    }
    
    updateUIForUser() {
        if (this.userProfile && this.userProfile.user !== 'Visiteur') {
            // Marquer comme utilisateur connecté
            const toggle = document.getElementById('chatbot-toggle');
            toggle.classList.add('user-connected');
            
            // Mettre à jour le message de bienvenue
            const welcomeText = document.querySelector('.bot-message .message-text');
            if (welcomeText) {
                welcomeText.innerHTML = `
                    🇩🇿 <strong>Bonjour ${this.userProfile.user} !</strong><br>
                    Bienvenue dans votre espace BBC School Algeria. Je connais votre profil : <strong>${this.getUserTypeLabel()}</strong>
                    <ul style="margin: 8px 0; padding-left: 20px;">
                        <li><strong>MES COURS</strong> : Votre programme personnel</li>
                        <li><strong>MES NOTES</strong> : Vos résultats individuels</li>
                        <li><strong>MON PLANNING</strong> : Votre emploi du temps</li>
                        <li><strong>SUPPORT</strong> : Aide personnalisée</li>
                    </ul>
                    Comment puis-je vous aider aujourd'hui ?
                `;
            }
            
            // Mettre à jour les infos profil
            const profileInfo = document.getElementById('user-profile-info');
            if (profileInfo) {
                profileInfo.textContent = `${this.getUserTypeLabel()} connecté(e)`;
            }
            
            // Mettre à jour les actions rapides
            this.updateQuickActions();
        }
    }
    
    getUserTypeLabel() {
        const labels = {
            'admin': 'Administrateur',
            'teacher': 'Enseignant(e)',
            'student': 'Étudiant(e)',
            'parent': 'Parent',
            'visitor': 'Visiteur'
        };
        return labels[this.userProfile?.userType] || 'Utilisateur';
    }
    
    updateQuickActions() {
        const container = document.getElementById('actions-buttons');
        const suggestions = this.userProfile?.suggestions || [];
        
        if (suggestions.length > 0) {
            container.innerHTML = '';
            suggestions.slice(0, 4).forEach((suggestion, index) => {
                const btn = document.createElement('button');
                btn.className = 'action-btn';
                btn.textContent = suggestion;
                btn.onclick = () => this.sendQuickMessage(suggestion);
                container.appendChild(btn);
            });
        }
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
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': this.csrfToken,
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            setTimeout(() => {
                this.hideTyping();
                if (data.success) {
                    this.addMessage(data.response, 'bot');
                    
                    // Log pour debug
                    if (data.userInfo) {
                        console.log('📊 Données utilisateur BBC School:', data.userInfo);
                    }
                } else {
                    this.addMessage('❌ Désolé, une erreur s\'est produite. Veuillez réessayer.', 'bot');
                }
            }, 1200);
            
        } catch (error) {
            console.error('🚨 Erreur BBC Chatbot:', error);
            setTimeout(() => {
                this.hideTyping();
                this.addMessage('🔌 Problème de connexion avec BBC School. Vérifiez votre réseau.', 'bot');
            }, 1200);
        }
    }
    
    sendQuickMessage(message) {
        const input = document.getElementById('chatbot-input');
        input.value = message;
        this.sendMessage();
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
                    '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="#2196F3" d="M12,3L1,9L12,15L21,12V17H23V10M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/></svg>' :
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
}

// Initialisation BBC School
document.addEventListener('DOMContentLoaded', () => {
    window.bbcSchoolChatbot = new BBCSchoolChatbot();
    console.log('🏫 BBC School Algeria Chatbot initialisé');
});

// Fonction globale pour les boutons d'action
function sendQuickMessage(message) {
    if (window.bbcSchoolChatbot) {
        window.bbcSchoolChatbot.sendQuickMessage(message);
    }
}
</script>