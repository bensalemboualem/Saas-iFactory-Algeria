// ========== HELP CHATBOT FUNCTIONS - IAFactory Algeria ==========

// Toggle fenêtre help
function toggleHelpWindow() {
    const helpWindow = document.getElementById('helpWindow');
    if (helpWindow) helpWindow.classList.toggle('open');
}

// Changer de mode
function setHelpMode(mode) {
    // Désactiver tous les boutons
    document.querySelectorAll('.iaf-chatbot-mode-btn').forEach(btn => btn.classList.remove('active'));

    // Activer le bouton sélectionné
    const modeBtn = document.getElementById(mode + 'ModeBtn');
    if (modeBtn) modeBtn.classList.add('active');

    // Afficher/masquer les éléments selon le mode
    const ragSelector = document.getElementById('helpRagSelector');
    const supportBanner = document.getElementById('helpSupportBanner');

    if (mode === 'rag') {
        if (ragSelector) ragSelector.style.display = 'block';
        if (supportBanner) supportBanner.style.display = 'none';
    } else if (mode === 'support') {
        if (ragSelector) ragSelector.style.display = 'none';
        if (supportBanner) supportBanner.style.display = 'block';
    } else {
        if (ragSelector) ragSelector.style.display = 'none';
        if (supportBanner) supportBanner.style.display = 'none';
    }
}

// Envoyer un message
async function sendHelpMessage() {
    const input = document.getElementById('helpInput');
    if (!input) return;
    const message = input.value.trim();

    if (!message) return;

    // Ajouter message utilisateur
    addHelpMessage(message, 'user');

    // Clear input
    input.value = '';

    // Afficher indicateur de chargement
    addHelpMessage('⏳ Réflexion en cours...', 'bot');

    try {
        // Récupérer le mode actuel
        const currentMode = document.querySelector('.iaf-chatbot-mode-btn.active')?.id?.replace('ModeBtn', '') || 'chat';
        const ragSelect = document.getElementById('helpRagSelect');
        const ragContext = ragSelect?.value || null;

        // Appel au backend sécurisé
        const response = await fetch('/api/help-chat/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                mode: currentMode,
                rag_context: currentMode === 'rag' ? ragContext : null
            })
        });

        // Supprimer le message de chargement
        const messagesContainer = document.getElementById('helpMessages');
        if (messagesContainer && messagesContainer.lastChild) {
            messagesContainer.removeChild(messagesContainer.lastChild);
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Erreur de communication avec le serveur');
        }

        const data = await response.json();
        const botResponse = data.response || 'Désolé, je n\'ai pas pu répondre.';

        addHelpMessage(botResponse, 'bot');

    } catch (error) {
        // Supprimer le message de chargement en cas d'erreur
        const messagesContainer = document.getElementById('helpMessages');
        if (messagesContainer && messagesContainer.lastChild) {
            messagesContainer.removeChild(messagesContainer.lastChild);
        }

        let errorMsg = '⚠️ Désolé, une erreur s\'est produite. Veuillez réessayer.';
        if (error.message && error.message !== 'Failed to fetch') {
            errorMsg = `⚠️ ${error.message}`;
        }

        addHelpMessage(errorMsg, 'bot');
        console.error('Help chat error:', error);
    }
}

// Ajouter un message
function addHelpMessage(text, sender) {
    const messagesContainer = document.getElementById('helpMessages');
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `iaf-chatbot-message iaf-chatbot-${sender}`;

    const avatar = sender === 'bot'
        ? `<img src="/assets/images/lala-fatma.png" alt="Dzir IA" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 8px rgba(0,132,61,0.3);">`
        : '👤';

    messageDiv.innerHTML = `
        <div class="iaf-chatbot-avatar">${avatar}</div>
        <div class="iaf-chatbot-bubble-msg">${text}</div>
    `;

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Gérer touche Enter
function handleHelpKeyPress(event) {
    if (event.key === 'Enter') {
        sendHelpMessage();
    }
}

console.log('✅ Chatbot Help functions loaded');
