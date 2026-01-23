{{-- BBC School Algeria - Bulle Chatbot Intégrée OnestSchool --}}
{{-- Visible sur toutes les pages frontend --}}

<!-- Font Awesome pour les icônes -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Bulle Chatbot BBC School -->
<div id="bbcChatBubble" class="bbc-chat-bubble">
    <!-- Logo BBC flottant -->
    <div class="chat-bubble-trigger" onclick="toggleBBCChat()">
        <div class="bubble-logo">
            <img src="{{ asset('img/logo BBC School.jpg') }}" alt="BBC School" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
            <div class="fallback-logo" style="display: none;">
                <i class="fas fa-graduation-cap"></i>
            </div>
        </div>
        <div class="bubble-notification" id="bbcNotification">
            <span>{{ ___('Besoin d\'aide ?') }}</span>
        </div>
        <div class="pulse-ring"></div>
    </div>

    <!-- Interface Chatbot -->
    <div class="chat-interface" id="bbcChatInterface" style="display: none;">
        <!-- Header avec logo BBC -->
        <div class="chat-header">
            <div class="header-info">
                <img src="{{ asset('img/logo BBC School.jpg') }}" alt="BBC School" class="header-logo" onerror="this.style.display='none'">
                <div class="header-text">
                    <h4>BBC School Algeria</h4>
                    <span class="status">{{ ___('Assistant en ligne') }}</span>
                </div>
            </div>
            <button class="close-btn" onclick="closeBBCChat()">
                <i class="fas fa-times"></i>
            </button>
        </div>

        <!-- Message de bienvenue -->
        <div class="chat-welcome">
            <div class="welcome-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="welcome-message">
                <h5>{{ ___('Bonjour !') }}</h5>
                <p>{{ ___('Je suis l\'assistant de BBC School Algeria. Comment puis-je vous aider ?') }}</p>
            </div>
        </div>

        <!-- Actions rapides pour BBC School -->
        <div class="quick-actions">
            <button class="action-btn" onclick="bbcAction('inscription')">
                <i class="fas fa-user-plus"></i>
                <span>{{ ___('Inscription') }}</span>
            </button>
            <button class="action-btn" onclick="bbcAction('info')">
                <i class="fas fa-info-circle"></i>
                <span>{{ ___('Informations') }}</span>
            </button>
            <button class="action-btn" onclick="bbcAction('tarifs')">
                <i class="fas fa-money-bill"></i>
                <span>{{ ___('Tarifs') }}</span>
            </button>
            <button class="action-btn" onclick="bbcAction('contact')">
                <i class="fas fa-phone"></i>
                <span>{{ ___('Contact') }}</span>
            </button>
        </div>

        <!-- Zone de conversation -->
        <div class="chat-messages" id="bbcMessages">
            <!-- Les messages apparaîtront ici -->
        </div>

        <!-- Input de message -->
        <div class="chat-input">
            <input type="text" id="bbcMessageInput" placeholder="{{ ___('Tapez votre message...') }}" maxlength="300">
            <button onclick="sendBBCMessage()">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>

        <!-- Footer avec liens BBC -->
        <div class="chat-footer">
            <div class="footer-links">
                <a href="https://www.facebook.com/bbc.bestbridgeforcreation/" target="_blank" class="social-link">
                    <i class="fab fa-facebook"></i>
                    <span>{{ ___('Facebook BBC') }}</span>
                </a>
                <a href="tel:+213xxxxxxxx" class="social-link">
                    <i class="fas fa-phone"></i>
                    <span>{{ ___('Appeler') }}</span>
                </a>
            </div>
        </div>
    </div>
</div>

<style>
/* BBC School Chatbot - Intégration OnestSchool */
.bbc-chat-bubble {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 10000;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Bulle déclencheur */
.chat-bubble-trigger {
    position: relative;
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, #1e3d59 0%, #ff6b35 100%);
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 20px rgba(30, 61, 89, 0.4);
    transition: all 0.3s ease;
    overflow: hidden;
}

.chat-bubble-trigger:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 25px rgba(30, 61, 89, 0.6);
}

.bubble-logo img {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    object-fit: cover;
}

.fallback-logo {
    width: 45px;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 24px;
}

/* Notification de la bulle */
.bubble-notification {
    position: absolute;
    bottom: 80px;
    right: 0;
    background: white;
    color: #1e3d59;
    padding: 12px 16px;
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    white-space: nowrap;
    font-size: 14px;
    font-weight: 600;
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.3s ease;
    pointer-events: none;
}

.bubble-notification::after {
    content: '';
    position: absolute;
    top: 100%;
    right: 20px;
    border: 8px solid transparent;
    border-top-color: white;
}

.chat-bubble-trigger:hover .bubble-notification {
    opacity: 1;
    transform: translateY(0);
}

/* Animation de pulsation */
.pulse-ring {
    position: absolute;
    top: -5px;
    left: -5px;
    right: -5px;
    bottom: -5px;
    border: 2px solid rgba(255, 107, 53, 0.6);
    border-radius: 50%;
    animation: pulse 2s ease-out infinite;
}

@keyframes pulse {
    0% {
        transform: scale(1);
        opacity: 0.6;
    }
    100% {
        transform: scale(1.3);
        opacity: 0;
    }
}

/* Interface du chat */
.chat-interface {
    position: absolute;
    bottom: 90px;
    right: 0;
    width: 350px;
    height: 500px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    animation: slideUpFade 0.3s ease-out;
}

@keyframes slideUpFade {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Header du chat */
.chat-header {
    background: linear-gradient(135deg, #1e3d59 0%, #2980b9 100%);
    color: white;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.header-logo {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.header-text h4 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
}

.header-text .status {
    font-size: 12px;
    opacity: 0.9;
}

.header-text .status::before {
    content: "●";
    color: #2ecc71;
    margin-right: 6px;
}

.close-btn {
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.3s ease;
}

.close-btn:hover {
    background: rgba(255,255,255,0.3);
}

/* Message de bienvenue */
.chat-welcome {
    padding: 20px;
    border-bottom: 1px solid #f0f0f0;
    display: flex;
    gap: 12px;
}

.welcome-avatar {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 18px;
    flex-shrink: 0;
}

.welcome-message h5 {
    margin: 0 0 8px 0;
    color: #1e3d59;
    font-size: 16px;
}

.welcome-message p {
    margin: 0;
    color: #666;
    font-size: 14px;
    line-height: 1.4;
}

/* Actions rapides */
.quick-actions {
    padding: 20px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    border-bottom: 1px solid #f0f0f0;
}

.action-btn {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 15px 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #495057;
}

.action-btn:hover {
    background: #ff6b35;
    color: white;
    border-color: #ff6b35;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

.action-btn i {
    font-size: 20px;
    color: #1e3d59;
}

.action-btn:hover i {
    color: white;
}

/* Zone de messages */
.chat-messages {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    background: #fafbfc;
}

.message {
    margin-bottom: 15px;
    display: flex;
    gap: 10px;
}

.message.user {
    justify-content: flex-end;
}

.message-content {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 14px;
    line-height: 1.4;
}

.message.bot .message-content {
    background: white;
    color: #333;
    border-bottom-left-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.message.user .message-content {
    background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
    color: white;
    border-bottom-right-radius: 6px;
}

/* Input de chat */
.chat-input {
    padding: 15px;
    border-top: 1px solid #e9ecef;
    display: flex;
    gap: 10px;
    background: white;
}

.chat-input input {
    flex: 1;
    border: 1px solid #e9ecef;
    border-radius: 25px;
    padding: 12px 16px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.3s ease;
}

.chat-input input:focus {
    border-color: #ff6b35;
}

.chat-input button {
    background: #ff6b35;
    color: white;
    border: none;
    width: 45px;
    height: 45px;
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

/* Footer avec liens */
.chat-footer {
    padding: 15px;
    background: #f8f9fa;
    border-top: 1px solid #e9ecef;
}

.footer-links {
    display: flex;
    justify-content: space-around;
}

.social-link {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #6c757d;
    text-decoration: none;
    font-size: 12px;
    transition: color 0.3s ease;
}

.social-link:hover {
    color: #ff6b35;
    text-decoration: none;
}

/* Responsive */
@media (max-width: 768px) {
    .chat-interface {
        width: 320px;
        height: 450px;
        right: -10px;
    }
    
    .bbc-chat-bubble {
        bottom: 20px;
        right: 20px;
    }
    
    .chat-bubble-trigger {
        width: 60px;
        height: 60px;
    }
    
    .bubble-logo img {
        width: 35px;
        height: 35px;
    }
}

/* Animation d'ouverture */
.chat-interface.opening {
    animation: slideUpFade 0.3s ease-out;
}

.chat-interface.closing {
    animation: slideDownFade 0.3s ease-out;
}

@keyframes slideDownFade {
    from {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
    to {
        opacity: 0;
        transform: translateY(20px) scale(0.95);
    }
}
</style>

<script>
// BBC School Chatbot - OnestSchool Integration
let bbcChatOpen = false;

// Données des réponses BBC School
const bbcResponses = {
    inscription: {
        title: "📝 Inscription BBC School Algeria",
        message: "Pour inscrire votre enfant à BBC School Algeria :\n\n• 📋 Documents : Acte de naissance, photos, certificat médical\n• 💰 Frais d'inscription : 15,000 DA\n• 📅 Période : Septembre - Octobre\n• 🏫 Niveaux : Maternelle au Cycle Moyen\n\nSouhaitez-vous prendre rendez-vous ?"
    },
    info: {
        title: "ℹ️ À propos de BBC School",
        message: "BBC School Algeria - École privée d'excellence :\n\n• 🎯 Programmes bilingues (Arabe/Français)\n• 👥 Classes à effectifs réduits\n• 🏆 Excellent taux de réussite au BEM\n• 🎨 Activités extrascolaires variées\n• 📍 Située à Alger\n\nNotre mission : Excellence, Innovation, Épanouissement"
    },
    tarifs: {
        title: "💰 Tarifs BBC School 2024-2025",
        message: "Frais de scolarité annuels :\n\n• 🧒 Maternelle : 120,000 DA\n• 📚 Primaire : 150,000 DA\n• 🎓 Cycle Moyen : 180,000 DA\n\n💳 Paiement en 3 tranches\n🎁 Réductions fratrie disponibles\n\nContactez-nous pour un devis personnalisé !"
    },
    contact: {
        title: "📞 Contacter BBC School",
        message: "BBC School Algeria - Coordonnées :\n\n• ☎️ Téléphone : +213-XX-XXX-XXX\n• 📧 Email : contact@bbcschoolalgeria.com\n• 🌐 Facebook : bbc.bestbridgeforcreation\n• 📍 Adresse : Alger, Algérie\n\n🕒 Horaires : Dimanche-Jeudi 8h-16h, Samedi 8h-12h\n\nNous sommes là pour vous aider !"
    }
};

function toggleBBCChat() {
    const chatInterface = document.getElementById('bbcChatInterface');
    const notification = document.getElementById('bbcNotification');
    
    if (!bbcChatOpen) {
        chatInterface.style.display = 'flex';
        chatInterface.classList.add('opening');
        bbcChatOpen = true;
        notification.style.display = 'none';
        
        // Focus sur l'input après animation
        setTimeout(() => {
            document.getElementById('bbcMessageInput').focus();
        }, 300);
    } else {
        closeBBCChat();
    }
}

function closeBBCChat() {
    const chatInterface = document.getElementById('bbcChatInterface');
    chatInterface.classList.add('closing');
    
    setTimeout(() => {
        chatInterface.style.display = 'none';
        chatInterface.classList.remove('opening', 'closing');
        bbcChatOpen = false;
    }, 300);
}

function bbcAction(actionType) {
    const response = bbcResponses[actionType];
    if (response) {
        addBBCMessage(response.message, 'bot', response.title);
    }
}

function sendBBCMessage() {
    const input = document.getElementById('bbcMessageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Ajouter le message utilisateur
    addBBCMessage(message, 'user');
    input.value = '';
    
    // Simuler réponse du bot
    setTimeout(() => {
        const botResponse = generateBBCResponse(message);
        addBBCMessage(botResponse, 'bot');
    }, 1000);
}

function addBBCMessage(text, sender, title = '') {
    const messagesContainer = document.getElementById('bbcMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    if (title) {
        text = `<strong>${title}</strong>\n\n${text}`;
    }
    
    messageDiv.innerHTML = `
        <div class="message-content">
            ${text.replace(/\n/g, '<br>')}
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function generateBBCResponse(message) {
    const msg = message.toLowerCase();
    
    if (msg.includes('inscription') || msg.includes('inscrire')) {
        return bbcResponses.inscription.message;
    } else if (msg.includes('tarif') || msg.includes('prix') || msg.includes('coût')) {
        return bbcResponses.tarifs.message;
    } else if (msg.includes('contact') || msg.includes('téléphone') || msg.includes('adresse')) {
        return bbcResponses.contact.message;
    } else if (msg.includes('info') || msg.includes('école') || msg.includes('à propos')) {
        return bbcResponses.info.message;
    } else {
        return "Merci pour votre question ! Je peux vous aider avec :\n\n📝 Inscriptions\n💰 Tarifs\nℹ️ Informations sur l'école\n📞 Contact\n\nQue souhaitez-vous savoir sur BBC School Algeria ?";
    }
}

// Gestion du clavier
document.addEventListener('keydown', function(e) {
    if (bbcChatOpen && e.key === 'Enter' && document.activeElement.id === 'bbcMessageInput') {
        e.preventDefault();
        sendBBCMessage();
    }
    if (e.key === 'Escape' && bbcChatOpen) {
        closeBBCChat();
    }
});

// Afficher la notification après 3 secondes
setTimeout(() => {
    const notification = document.getElementById('bbcNotification');
    if (notification && !bbcChatOpen) {
        notification.style.display = 'block';
        
        // Masquer après 5 secondes
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000);
    }
}, 3000);

console.log('🎓 BBC School Algeria Chatbot chargé dans OnestSchool !');
</script>