<?php
/**
 * BBC School Algeria - Intégration OnestSchool
 * Module d'intégration du chatbot IA dans la plateforme OnestSchool
 */

// Ajouter le menu chatbot dans la navigation OnestSchool
?>

<!-- Ajout du bouton chatbot flottant -->
<div id="bbcChatbotFloating" class="chatbot-floating">
    <div class="chatbot-toggle" onclick="toggleChatbot()">
        <i class="fas fa-robot"></i>
        <span class="notification-badge" id="chatNotification">3</span>
    </div>
    
    <div class="chatbot-popup" id="chatbotPopup" style="display: none;">
        <div class="chatbot-header">
            <div class="chatbot-logo">
                <img src="assets/img/bbc-logo.jpg" alt="BBC IA">
                <span>Assistant IA BBC</span>
            </div>
            <div class="chatbot-actions">
                <button onclick="openFullChatbot()"><i class="fas fa-expand"></i></button>
                <button onclick="toggleChatbot()"><i class="fas fa-times"></i></button>
            </div>
        </div>
        
        <div class="chatbot-content">
            <div class="quick-actions">
                <button class="quick-btn" onclick="quickAction('help')">
                    <i class="fas fa-question-circle"></i>
                    <span>Aide Rapide</span>
                </button>
                <button class="quick-btn" onclick="quickAction('grades')">
                    <i class="fas fa-chart-line"></i>
                    <span>Mes Notes</span>
                </button>
                <button class="quick-btn" onclick="quickAction('schedule')">
                    <i class="fas fa-calendar"></i>
                    <span>Planning</span>
                </button>
                <button class="quick-btn" onclick="quickAction('contact')">
                    <i class="fas fa-phone"></i>
                    <span>Contact</span>
                </button>
            </div>
            
            <div class="chat-preview">
                <div class="message bot-message">
                    <i class="fas fa-robot"></i>
                    <span>Bonjour ! Comment puis-je vous aider aujourd'hui ?</span>
                </div>
            </div>
            
            <div class="chat-input-mini">
                <input type="text" placeholder="Tapez votre question...">
                <button><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    </div>
</div>

<style>
/* Chatbot Flottant OnestSchool Integration */
.chatbot-floating {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
}

.chatbot-toggle {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #1e3d59 0%, #ff6b35 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
    position: relative;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.chatbot-toggle:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}

.notification-badge {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #e74c3c;
    color: white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    font-size: 0.7rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

.chatbot-popup {
    position: absolute;
    bottom: 80px;
    right: 0;
    width: 350px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    overflow: hidden;
    border: 1px solid #ddd;
}

.chatbot-header {
    background: linear-gradient(135deg, #1e3d59 0%, #2980b9 100%);
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chatbot-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.chatbot-logo img {
    width: 30px;
    height: 30px;
    border-radius: 5px;
}

.chatbot-actions {
    display: flex;
    gap: 5px;
}

.chatbot-actions button {
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    padding: 5px 8px;
    border-radius: 5px;
    cursor: pointer;
}

.chatbot-content {
    padding: 20px;
}

.quick-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 15px;
}

.quick-btn {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    text-align: center;
}

.quick-btn:hover {
    background: #e9ecef;
    border-color: #ff6b35;
    color: #ff6b35;
}

.quick-btn i {
    font-size: 1.2rem;
    color: #1e3d59;
}

.quick-btn span {
    font-size: 0.8rem;
    font-weight: 500;
}

.chat-preview {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 15px;
}

.message {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
}

.message i {
    color: #1e3d59;
}

.chat-input-mini {
    display: flex;
    gap: 8px;
}

.chat-input-mini input {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #dee2e6;
    border-radius: 20px;
    outline: none;
}

.chat-input-mini button {
    background: #ff6b35;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 50%;
    cursor: pointer;
}

/* Responsive */
@media (max-width: 768px) {
    .chatbot-popup {
        width: 300px;
        right: -20px;
    }
    
    .chatbot-floating {
        bottom: 15px;
        right: 15px;
    }
}
</style>

<script>
// Fonction pour basculer le chatbot
function toggleChatbot() {
    const popup = document.getElementById('chatbotPopup');
    const notification = document.getElementById('chatNotification');
    
    if (popup.style.display === 'none' || popup.style.display === '') {
        popup.style.display = 'block';
        popup.style.animation = 'slideUp 0.3s ease';
        notification.style.display = 'none';
    } else {
        popup.style.animation = 'slideDown 0.3s ease';
        setTimeout(() => {
            popup.style.display = 'none';
        }, 300);
    }
}

// Fonction pour ouvrir le chatbot en plein écran
function openFullChatbot() {
    window.open('bbc-ia-vitrine.html', '_blank', 'width=1200,height=800');
}

// Actions rapides
function quickAction(action) {
    console.log(`🎯 Action rapide: ${action}`);
    
    switch(action) {
        case 'help':
            showQuickHelp();
            break;
        case 'grades':
            showGrades();
            break;
        case 'schedule':
            showSchedule();
            break;
        case 'contact':
            showContact();
            break;
    }
}

function showQuickHelp() {
    alert('🤖 Assistant IA BBC School:\n\n• Aide aux devoirs\n• Information sur les notes\n• Planning des cours\n• Contact avec les enseignants\n• Paiements en ligne');
}

function showGrades() {
    // Intégration avec OnestSchool pour afficher les notes
    if (typeof showStudentGrades === 'function') {
        showStudentGrades();
    } else {
        alert('📊 Vos dernières notes:\n\n• Mathématiques: 16/20\n• Français: 14/20\n• Sciences: 18/20\n• Anglais: 15/20');
    }
}

function showSchedule() {
    alert('📅 Votre planning aujourd\'hui:\n\n• 08h00: Mathématiques\n• 10h00: Français\n• 14h00: Sciences\n• 16h00: Sport');
}

function showContact() {
    alert('📞 Contacts BBC School Algeria:\n\n• Téléphone: +213-XX-XXX-XXX\n• Email: contact@bbcschoolalgeria.com\n• Facebook: bbc.bestbridgeforcreation\n• Adresse: Alger, Algérie');
}

// Animation CSS keyframes
const style = document.createElement('style');
style.textContent = `
@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes slideDown {
    from { transform: translateY(0); opacity: 1; }
    to { transform: translateY(20px); opacity: 0; }
}
`;
document.head.appendChild(style);

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    console.log('🤖 Chatbot BBC intégré à OnestSchool!');
    
    // Simuler des notifications
    setTimeout(() => {
        const notification = document.getElementById('chatNotification');
        if (notification) {
            notification.textContent = Math.floor(Math.random() * 5) + 1;
        }
    }, 3000);
});
</script>