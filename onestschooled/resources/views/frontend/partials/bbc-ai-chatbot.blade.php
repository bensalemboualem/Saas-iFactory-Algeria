
<!-- BBC School Algeria - Chatbot IA Intégré -->
<div id="bbc-ai-chatbot" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
    <div id="chat-trigger" style="width: 60px; height: 60px; background: linear-gradient(135deg, #392C7D, #FF5170); border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 20px rgba(0,0,0,0.3); transition: all 0.3s ease;">
        <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12c0 1.54.36 3.04.97 4.37L1 23l6.63-1.97C9.96 21.64 11.46 22 13 22h7c1.1 0 2-.9 2-2V12c0-5.52-4.48-10-10-10z"/>
        </svg>
    </div>
    
    <div id="chat-window" style="display: none; width: 350px; height: 500px; background: white; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); position: absolute; bottom: 70px; right: 0; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #392C7D, #FF5170); color: white; padding: 20px; text-align: center;">
            <h4 style="margin: 0; font-size: 16px;">🤖 Assistant IA BBC School</h4>
            <p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.9;">Posez vos questions sur notre école</p>
        </div>
        
        <div id="chat-messages" style="height: 340px; overflow-y: auto; padding: 15px; background: #f8f9fa;">
            <div class="message bot-message" style="margin-bottom: 15px;">
                <div style="background: #e9ecef; padding: 10px; border-radius: 15px; font-size: 14px;">
                    👋 Bonjour ! Je suis l'assistant IA de BBC School Algeria. Comment puis-je vous aider ?
                </div>
            </div>
        </div>
        
        <div style="padding: 15px; border-top: 1px solid #eee; background: white;">
            <div style="display: flex; gap: 10px;">
                <input type="text" id="chat-input" placeholder="Tapez votre message..." style="flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 25px; outline: none; font-size: 14px;">
                <button id="send-btn" style="background: #392C7D; color: white; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>
</div>

<script>
// BBC School Algeria - Chatbot IA fonctionnel
document.addEventListener("DOMContentLoaded", function() {
    const trigger = document.getElementById("chat-trigger");
    const window = document.getElementById("chat-window");
    const input = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const messages = document.getElementById("chat-messages");
    
    let isOpen = false;
    
    // Ouvrir/fermer le chat
    trigger.addEventListener("click", function() {
        isOpen = !isOpen;
        window.style.display = isOpen ? "block" : "none";
        if (isOpen) {
            input.focus();
        }
    });
    
    // Base de connaissances BBC School Algeria
    const bbcKnowledge = {
        "admission|inscription|rentrée": "📚 Les inscriptions pour l'année 2024-2025 sont ouvertes ! BBC School Algeria accueille les élèves de la Maternelle au Cycle Moyen. Contactez-nous au secrétariat pour plus d'informations.",
        "transport|bus|navette": "🚌 Nous proposons un service de transport scolaire avec des véhicules Mercedes Sprinter sécurisés couvrant toute la région. Plusieurs zones de ramassage disponibles.",
        "cantine|repas|déjeuner": "🍽️ Notre cantine propose des repas halal équilibrés et nutritifs préparés selon les normes d'hygiène. Menu varié et adapté aux besoins des élèves.",
        "frais|tarifs|prix": "💰 Les frais de scolarité varient selon le niveau : Maternelle (120 000 DZD), Primaire (150 000 DZD), Cycle Moyen (180 000 DZD). Transport et cantine en supplément.",
        "programme|matières|cours": "📖 Programmes conformes au ministère algérien. Enseignement bilingue français-arabe. Préparation spécialisée au BEM avec accompagnement personnalisé.",
        "horaires|emploi du temps": "⏰ Horaires : 8h-12h (matin) et 13h-17h (après-midi). Emploi du temps adapté selon les niveaux. Possibilité de journée complète avec cantine.",
        "bem|examens": "🎓 Excellent taux de réussite au BEM ! Préparation intensive avec cours de soutien et examens blancs réguliers.",
        "salles|laboratoires|infrastructure": "🏫 Infrastructure moderne : 30 salles de classe, laboratoires de sciences, salle informatique, bibliothèque, gymnase et espaces verts.",
        "contact|téléphone|adresse": "📞 Contactez BBC School Algeria au secrétariat. Nous sommes disponibles pour répondre à toutes vos questions sur notre établissement.",
        "enseignants|professeurs|équipe": "👨‍🏫 Équipe pédagogique qualifiée de 45 enseignants expérimentés. Formation continue et suivi personnalisé de chaque élève."
    };
    
    // Fonction pour envoyer un message
    function sendMessage() {
        const text = input.value.trim();
        if (!text) return;
        
        // Ajouter message utilisateur
        addMessage(text, "user");
        input.value = "";
        
        // Simuler la réflexion de l'IA
        setTimeout(() => {
            addMessage("💭 Je réfléchis...", "bot");
            
            setTimeout(() => {
                removeLastBotMessage();
                const response = getBBCResponse(text);
                addMessage(response, "bot");
            }, 1500);
        }, 500);
    }
    
    // Réponse intelligente basée sur la base de connaissances
    function getBBCResponse(question) {
        const lowerQuestion = question.toLowerCase();
        
        for (const [keywords, response] of Object.entries(bbcKnowledge)) {
            const keywordList = keywords.split("|");
            if (keywordList.some(keyword => lowerQuestion.includes(keyword))) {
                return response;
            }
        }
        
        // Réponse par défaut
        return "🤔 Je n'ai pas d'information spécifique sur ce sujet. Pouvez-vous me poser une question sur nos programmes, frais, transport, cantine, examens ou infrastructure ? Ou contactez directement notre secrétariat !";
    }
    
    // Ajouter un message au chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.className = "message " + sender + "-message";
        messageDiv.style.marginBottom = "15px";
        
        const bubble = document.createElement("div");
        bubble.style.padding = "10px";
        bubble.style.borderRadius = "15px";
        bubble.style.fontSize = "14px";
        bubble.style.lineHeight = "1.4";
        
        if (sender === "user") {
            bubble.style.background = "#392C7D";
            bubble.style.color = "white";
            bubble.style.marginLeft = "50px";
            messageDiv.style.textAlign = "right";
        } else {
            bubble.style.background = "#e9ecef";
            bubble.style.color = "#333";
            bubble.style.marginRight = "50px";
        }
        
        bubble.textContent = text;
        messageDiv.appendChild(bubble);
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight;
    }
    
    // Supprimer le dernier message bot (pour remplacer "Je réfléchis...")
    function removeLastBotMessage() {
        const botMessages = messages.querySelectorAll(".bot-message");
        if (botMessages.length > 1) {
            botMessages[botMessages.length - 1].remove();
        }
    }
    
    // Events
    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
    
    // Messages de suggestions au démarrage
    setTimeout(() => {
        addMessage("💡 Voici quelques questions que vous pouvez me poser :", "bot");
        setTimeout(() => addMessage("• Comment s'inscrire à BBC School ?", "bot"), 1000);
        setTimeout(() => addMessage("• Quels sont les frais de scolarité ?", "bot"), 2000);
        setTimeout(() => addMessage("• Avez-vous un service de transport ?", "bot"), 3000);
    }, 2000);
});
</script>