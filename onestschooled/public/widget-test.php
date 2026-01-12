<?php
// Widget de test standalone pour démonstration
// Ce fichier sera inclus dans le test
?>

{{-- BBC School Algeria - Assistant IA Widget Test --}}
<div id="bbcChatbotWidget" class="bbc-chatbot-widget">
    <!-- Bouton d'activation -->
    <div class="chatbot-trigger" onclick="toggleBBCChatbot()">
        <div class="trigger-icon">
            <i class="fas fa-graduation-cap"></i>
        </div>
        <div class="trigger-text">
            <span>Aide BBC School</span>
            <small>Inscription • Info • Support</small>
        </div>
        <div class="notification-dot" id="chatNotification" style="display: none;"></div>
    </div>

    <!-- Interface Chat -->
    <div class="chatbot-interface" id="bbcChatInterface" style="display: none;">
        <div class="chat-header">
            <div class="header-left">
                <img src="img/logo BBC School.jpg" alt="BBC" class="logo-mini" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNCIgZmlsbD0iIzFFM0Q1OSIvPgo8dGV4dCB4PSIxNiIgeT0iMjAiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5CQkM8L3RleHQ+Cjwvc3ZnPgo='">
                <div>
                    <h4>Assistant BBC School</h4>
                    <span class="status online">En ligne</span>
                </div>
            </div>
            <div class="header-actions">
                <button onclick="minimizeBBCChat()" title="Réduire">
                    <i class="fas fa-minus"></i>
                </button>
                <button onclick="closeBBCChat()" title="Fermer">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>

        <!-- Actions Rapides -->
        <div class="quick-actions">
            <div class="action-title">Comment puis-je vous aider ?</div>
            <div class="actions-grid">
                <button class="action-btn" onclick="bbcQuickAction('inscription')">
                    <i class="fas fa-user-plus"></i>
                    <span>Inscription</span>
                </button>
                <button class="action-btn" onclick="bbcQuickAction('infos')">
                    <i class="fas fa-info-circle"></i>
                    <span>Informations</span>
                </button>
                <button class="action-btn" onclick="bbcQuickAction('tarifs')">
                    <i class="fas fa-euro-sign"></i>
                    <span>Tarifs</span>
                </button>
                <button class="action-btn" onclick="bbcQuickAction('contact')">
                    <i class="fas fa-phone"></i>
                    <span>Contact</span>
                </button>
                <button class="action-btn" onclick="bbcQuickAction('programmes')">
                    <i class="fas fa-book"></i>
                    <span>Programmes</span>
                </button>
                <button class="action-btn" onclick="bbcQuickAction('visite')">
                    <i class="fas fa-eye"></i>
                    <span>Visite École</span>
                </button>
            </div>
        </div>

        <!-- Zone de Chat -->
        <div class="chat-messages" id="bbcChatMessages">
            <div class="welcome-message">
                <div class="bot-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>Bonjour ! Je suis l'assistant de BBC School Algeria.</p>
                    <p>Je peux vous aider pour :</p>
                    <ul>
                        <li>📝 Inscription de votre enfant</li>
                        <li>📋 Informations sur nos programmes</li>
                        <li>💰 Tarifs et paiements</li>
                        <li>📞 Prendre rendez-vous</li>
                        <li>🏫 Organiser une visite</li>
                    </ul>
                    <p>Que souhaitez-vous savoir ?</p>
                </div>
            </div>
        </div>

        <!-- Input de Chat -->
        <div class="chat-input">
            <input type="text" id="bbcMessageInput" placeholder="Posez votre question..." maxlength="500">
            <button onclick="sendBBCMessage()">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>

        <!-- Footer avec liens utiles -->
        <div class="chat-footer">
            <div class="footer-links">
                <a href="https://www.facebook.com/bbc.bestbridgeforcreation/" target="_blank">
                    <i class="fab fa-facebook"></i> Notre Facebook
                </a>
                <a href="tel:+213xxxxxxxx">
                    <i class="fas fa-phone"></i> Appeler
                </a>
                <a href="#" onclick="alert('Intégré dans OnestSchool !')">
                    <i class="fas fa-graduation-cap"></i> OnestSchool
                </a>
            </div>
        </div>
    </div>
</div>

<style>
/* BBC School Chatbot Widget Styles - Test Version */
.bbc-chatbot-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.chatbot-trigger {
    background: linear-gradient(135deg, #1e3d59 0%, #ff6b35 100%);
    color: white;
    padding: 16px 20px;
    border-radius: 50px;
    box-shadow: 0 4px 20px rgba(30, 61, 89, 0.3);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.3s ease;
    max-width: 280px;
    position: relative;
}

.chatbot-trigger:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(30, 61, 89, 0.4);
}

.trigger-icon {
    background: rgba(255, 255, 255, 0.2);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

.trigger-text span {
    font-weight: 600;
    font-size: 14px;
    display: block;
}

.trigger-text small {
    font-size: 11px;
    opacity: 0.9;
}

.notification-dot {
    position: absolute;
    top: 8px;
    right: 15px;
    width: 12px;
    height: 12px;
    background: #e74c3c;
    border-radius: 50%;
    border: 2px solid white;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.7; }
}

.chatbot-interface {
    position: absolute;
    bottom: 80px;
    right: 0;
    width: 380px;
    height: 550px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    border: 1px solid #e1e5e9;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.chat-header {
    background: linear-gradient(135deg, #1e3d59 0%, #2980b9 100%);
    color: white;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-mini {
    width: 32px;
    height: 32px;
    border-radius: 6px;
    object-fit: cover;
}

.header-left h4 {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
}

.status {
    font-size: 11px;
    opacity: 0.9;
}

.status.online::before {
    content: "●";
    color: #2ecc71;
    margin-right: 4px;
}

.header-actions {
    display: flex;
    gap: 8px;
}

.header-actions button {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
}

.quick-actions {
    padding: 20px;
    border-bottom: 1px solid #f0f2f5;
}

.action-title {
    font-weight: 600;
    color: #1e3d59;
    margin-bottom: 16px;
    font-size: 14px;
}

.actions-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.action-btn {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 12px 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #495057;
}

.action-btn:hover {
    background: #ff6b35;
    color: white;
    border-color: #ff6b35;
    transform: translateY(-1px);
}

.action-btn i {
    font-size: 16px;
    color: #1e3d59;
}

.action-btn:hover i {
    color: white;
}

.chat-messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: #fafbfc;
}

.welcome-message, .bot-message {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}

.bot-avatar {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #1e3d59 0%, #ff6b35 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 14px;
    flex-shrink: 0;
}

.message-content {
    background: white;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    font-size: 14px;
    line-height: 1.5;
}

.message-content ul {
    margin: 12px 0;
    padding-left: 20px;
}

.message-content li {
    margin: 6px 0;
}

.user-message {
    display: flex;
    justify-content: flex-end;
    margin: 16px 0;
}

.user-message .message-content {
    background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
    color: white;
    max-width: 80%;
}

.chat-input {
    padding: 16px 20px;
    border-top: 1px solid #e9ecef;
    display: flex;
    gap: 12px;
    background: white;
}

.chat-input input {
    flex: 1;
    border: 1px solid #e9ecef;
    border-radius: 20px;
    padding: 10px 16px;
    font-size: 14px;
    outline: none;
}

.chat-input input:focus {
    border-color: #ff6b35;
}

.chat-input button {
    background: #ff6b35;
    color: white;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.chat-input button:hover {
    background: #e55a2b;
    transform: scale(1.05);
}

.chat-footer {
    padding: 12px 20px;
    background: #f8f9fa;
    border-top: 1px solid #e9ecef;
}

.footer-links {
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
}

.footer-links a {
    color: #6c757d;
    text-decoration: none;
    font-size: 11px;
    display: flex;
    align-items: center;
    gap: 4px;
    transition: color 0.3s ease;
}

.footer-links a:hover {
    color: #ff6b35;
}

/* Responsive */
@media (max-width: 480px) {
    .chatbot-interface {
        width: 320px;
        height: 500px;
        right: -10px;
    }
    
    .chatbot-trigger {
        max-width: 250px;
    }
    
    .actions-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Animations */
@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes slideDown {
    from { transform: translateY(0); opacity: 1; }
    to { transform: translateY(20px); opacity: 0; }
}
</style>

<script>
// BBC School Chatbot Functionality - Test Version
let bbcChatOpen = false;
let bbcChatMinimized = false;

function toggleBBCChatbot() {
    const chatInterface = document.getElementById('bbcChatInterface');
    const notification = document.getElementById('chatNotification');
    
    if (!bbcChatOpen) {
        chatInterface.style.display = 'flex';
        chatInterface.style.animation = 'slideUp 0.3s ease';
        bbcChatOpen = true;
        notification.style.display = 'none';
        
        setTimeout(() => {
            document.getElementById('bbcMessageInput').focus();
        }, 300);
    } else {
        closeBBCChat();
    }
}

function closeBBCChat() {
    const chatInterface = document.getElementById('bbcChatInterface');
    chatInterface.style.animation = 'slideDown 0.3s ease';
    setTimeout(() => {
        chatInterface.style.display = 'none';
        bbcChatOpen = false;
    }, 300);
}

function minimizeBBCChat() {
    bbcChatMinimized = !bbcChatMinimized;
}

function bbcQuickAction(action) {
    const responses = {
        inscription: {
            title: "📝 Inscription à BBC School Algeria",
            content: `Pour inscrire votre enfant chez nous :\n\n**📋 Documents requis :**\n• Acte de naissance\n• Photos d'identité\n• Certificat médical\n• Relevé de notes (si transfert)\n\n**💰 Frais d'inscription :** 15,000 DA\n**📅 Période :** Septembre - Octobre\n\n**📞 Contact direct :** +213-XX-XXX-XXX\n\nSouhaitez-vous prendre rendez-vous pour finaliser l'inscription ?`
        },
        infos: {
            title: "ℹ️ Informations BBC School Algeria",
            content: `**🏫 À propos de BBC School :**\n• École privée d'excellence\n• Programmes bilingues (Arabe/Français)\n• Classes de la maternelle au lycée\n• Effectifs réduits (max 25 élèves/classe)\n\n**🎯 Notre mission :**\n"Excellence • Innovation • Épanouissement"\n\n**📍 Adresse :** Alger, Algérie\n**🌐 Facebook :** bbc.bestbridgeforcreation\n\nQue souhaitez-vous savoir de plus ?`
        },
        tarifs: {
            title: "💰 Tarifs BBC School Algeria",
            content: `**📊 Frais de scolarité 2024-2025 :**\n\n**🧒 Maternelle :** 120,000 DA/an\n**📚 Primaire :** 150,000 DA/an\n**🎓 Moyen :** 180,000 DA/an\n**📖 Lycée :** 200,000 DA/an\n\n**💳 Modalités de paiement :**\n• 3 tranches possibles\n• Réduction fratrie : -10%\n• Paiement anticipé : -5%\n\n**📞 Pour un devis personnalisé :** +213-XX-XXX-XXX`
        },
        contact: {
            title: "📞 Nous Contacter",
            content: `**🏫 BBC School Algeria**\n\n**📍 Adresse :** Alger, Algérie\n**☎️ Téléphone :** +213-XX-XXX-XXX\n**📧 Email :** contact@bbcschoolalgeria.com\n**🌐 Facebook :** facebook.com/bbc.bestbridgeforcreation\n\n**🕒 Horaires d'accueil :**\n• Dimanche - Jeudi : 8h00 - 16h00\n• Samedi : 8h00 - 12h00\n\n**📅 Prendre rendez-vous :**\nContactez-nous pour fixer un entretien !`
        },
        programmes: {
            title: "📚 Nos Programmes Éducatifs",
            content: `**🎯 Programmes BBC School :**\n\n**🧒 Maternelle (3-5 ans) :**\n• Éveil et socialisation\n• Préparation à la lecture\n• Activités ludiques\n\n**📚 Primaire (6-10 ans) :**\n• Programme national renforcé\n• Langues : Arabe, Français, Anglais\n• Sciences et mathématiques\n\n**🎓 Moyen & Lycée :**\n• Sections scientifiques\n• Préparation BAC\n• Orientation universitaire\n\n**🌟 Options spéciales :**\n• Informatique dès le primaire\n• Arts et sports\n• Clubs de sciences`
        },
        visite: {
            title: "👁️ Visite de l'École",
            content: `**🏫 Découvrir BBC School Algeria**\n\n**📅 Journées portes ouvertes :**\n• Chaque samedi de 9h à 12h\n• Visite guidée gratuite\n• Rencontre avec l'équipe pédagogique\n\n**👨‍🏫 Ce que vous verrez :**\n• Salles de classe équipées\n• Laboratoires de sciences\n• Bibliothèque et salle informatique\n• Espaces de jeux et sport\n\n**📞 Réserver votre visite :**\nAppelez-nous au +213-XX-XXX-XXX\n\nPréférez-vous une visite ce weekend ?`
        }
    };

    const response = responses[action];
    if (response) {
        addBBCMessage(response.content, 'bot', response.title);
    }
}

function sendBBCMessage() {
    const input = document.getElementById('bbcMessageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    addBBCMessage(message, 'user');
    input.value = '';
    
    setTimeout(() => {
        const botResponse = generateBBCResponse(message);
        addBBCMessage(botResponse, 'bot');
    }, 1000);
}

function addBBCMessage(message, sender, title = '') {
    const chatMessages = document.getElementById('bbcChatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
    
    if (sender === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content">
                ${escapeHtml(message)}
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="bot-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                ${title ? `<strong>${title}</strong><br><br>` : ''}
                ${message.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}
            </div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function generateBBCResponse(message) {
    const msg = message.toLowerCase();
    
    if (msg.includes('inscription') || msg.includes('inscrire')) {
        return `Pour l'inscription à BBC School Algeria, vous avez besoin de :\n\n📋 **Documents :**\n• Acte de naissance\n• Photos d'identité\n• Certificat médical\n• Bulletin scolaire\n\n💰 **Frais :** 15,000 DA d'inscription + frais de scolarité\n\n📞 **Contact :** +213-XX-XXX-XXX\n\nSouhaitez-vous prendre rendez-vous ?`;
    }
    
    if (msg.includes('tarif') || msg.includes('prix') || msg.includes('coût')) {
        return `**💰 Nos tarifs 2024-2025 :**\n\n🧒 Maternelle : 120,000 DA/an\n📚 Primaire : 150,000 DA/an\n🎓 Moyen : 180,000 DA/an\n📖 Lycée : 200,000 DA/an\n\nPaiement en 3 tranches possible. Réductions disponibles !`;
    }
    
    if (msg.includes('contact') || msg.includes('téléphone') || msg.includes('adresse')) {
        return `📞 **Nous contacter :**\n\n☎️ Tél : +213-XX-XXX-XXX\n📧 Email : contact@bbcschoolalgeria.com\n🌐 Facebook : bbc.bestbridgeforcreation\n📍 Adresse : Alger, Algérie\n\nHoraires : Dim-Jeu 8h-16h, Sam 8h-12h`;
    }
    
    return `Merci pour votre question ! Je peux vous aider avec :\n\n📝 Inscriptions et admissions\n💰 Tarifs et paiements\n📚 Programmes éducatifs\n📞 Informations de contact\n👁️ Visites de l'école\n\nQue souhaitez-vous savoir ?`;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Gestion des touches
document.addEventListener('keydown', function(e) {
    if (bbcChatOpen && e.key === 'Enter' && document.activeElement.id === 'bbcMessageInput') {
        e.preventDefault();
        sendBBCMessage();
    }
    if (e.key === 'Escape' && bbcChatOpen) {
        closeBBCChat();
    }
});

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    console.log('🤖 BBC School Chatbot Test Version loaded!');
});
</script>