#!/usr/bin/env python3
"""Insert chatbot help into creative-studio"""

# Read creative-studio
with open('/opt/iafactory-rag-dz/apps/creative-studio/index.html', 'r') as f:
    content = f.read()

# CSS for chatbot
css = '''
        /* ========== CHATBOT HELP ========== */
        .help-btn {
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00a651, #00d66a);
            border: none;
            cursor: pointer;
            color: white;
            font-size: 24px;
            box-shadow: 0 4px 20px rgba(0, 166, 81, 0.4);
            z-index: 9999;
            transition: all 0.3s ease;
        }
        .help-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(0, 166, 81, 0.6);
        }
        .help-window {
            position: fixed;
            bottom: 100px;
            right: 24px;
            width: 380px;
            height: 500px;
            background: var(--bg-card, #1a1a2e);
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            display: none;
            flex-direction: column;
            z-index: 9998;
            overflow: hidden;
            border: 1px solid var(--border-color, rgba(255,255,255,0.1));
        }
        .help-window.open {
            display: flex;
        }
        .help-header {
            padding: 16px;
            background: linear-gradient(135deg, #00a651, #00d66a);
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .help-header h3 { margin: 0; font-size: 16px; }
        .close-help-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
        }
        .help-modes {
            display: flex;
            padding: 8px;
            gap: 4px;
            background: var(--bg-secondary, #0d0d1a);
        }
        .help-mode-btn {
            flex: 1;
            padding: 8px;
            border: none;
            background: transparent;
            color: var(--text-secondary, #888);
            cursor: pointer;
            border-radius: 8px;
            font-size: 12px;
            transition: all 0.2s;
        }
        .help-mode-btn.active {
            background: var(--accent-primary, #00a651);
            color: white;
        }
        .help-messages {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
        }
        .help-message {
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
        }
        .help-message.help-user {
            justify-content: flex-end;
        }
        .help-message.help-user .help-bubble-msg {
            background: var(--accent-primary, #00a651);
            color: white;
        }
        .help-bubble-msg {
            background: var(--bg-secondary, #252542);
            padding: 10px 14px;
            border-radius: 12px;
            max-width: 80%;
            color: var(--text-primary, #fff);
            font-size: 14px;
            line-height: 1.4;
        }
        .help-input {
            display: flex;
            padding: 12px;
            gap: 8px;
            border-top: 1px solid var(--border-color, rgba(255,255,255,0.1));
        }
        .help-input input {
            flex: 1;
            padding: 10px 14px;
            border: 1px solid var(--border-color, rgba(255,255,255,0.1));
            border-radius: 20px;
            background: var(--bg-secondary, #0d0d1a);
            color: var(--text-primary, #fff);
            outline: none;
        }
        .help-send-btn {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: none;
            background: var(--accent-primary, #00a651);
            color: white;
            cursor: pointer;
            transition: all 0.2s;
        }
        .help-send-btn:hover {
            transform: scale(1.1);
        }
        .help-rag-selector {
            padding: 8px 12px;
            background: var(--bg-secondary, #0d0d1a);
        }
        .help-rag-selector select {
            width: 100%;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background: var(--bg-card);
            color: var(--text-primary);
        }
        .help-support-banner {
            padding: 12px;
            background: rgba(245, 158, 11, 0.2);
            text-align: center;
            color: var(--text-primary);
        }
        .back-to-ai-btn {
            margin-top: 8px;
            padding: 6px 12px;
            border-radius: 6px;
            border: none;
            background: var(--accent-primary, #00a651);
            color: white;
            cursor: pointer;
        }
'''

# HTML for chatbot
html = '''
    <!-- ========== CHATBOT HELP ========== -->
    <button class="help-btn" onclick="toggleHelpWindow()">💬</button>
    <div class="help-window" id="helpWindow">
        <div class="help-header">
            <h3>🤖 Dzir IA</h3>
            <button class="close-help-btn" onclick="toggleHelpWindow()">×</button>
        </div>
        <div class="help-modes">
            <button class="help-mode-btn active" id="chatModeBtn" onclick="setHelpMode('chat')">💬 Chat IA</button>
            <button class="help-mode-btn" id="ragModeBtn" onclick="setHelpMode('rag')">🔍 RAG</button>
            <button class="help-mode-btn" id="supportModeBtn" onclick="setHelpMode('support')">📞 Support</button>
        </div>
        <div class="help-rag-selector" id="helpRagSelector" style="display:none;">
            <select id="helpRagSelect">
                <option value="DZ">🇩🇿 Business DZ</option>
                <option value="ALL">🌍 Tous les RAG</option>
            </select>
        </div>
        <div class="help-support-banner" id="helpSupportBanner" style="display:none;">
            ⚠️ Mode support humain activé<br>
            <button class="back-to-ai-btn" onclick="setHelpMode('chat')">🤖 Retour IA</button>
        </div>
        <div class="help-messages" id="helpMessages">
            <div class="help-message help-bot">
                <div class="help-bubble-msg">👋 Bonjour ! Je suis <strong>Dzir IA</strong>. Comment puis-je vous aider ?</div>
            </div>
        </div>
        <div class="help-input">
            <input type="text" id="helpInput" placeholder="Tapez votre message..." onkeypress="if(event.key==='Enter')sendHelpMessage()">
            <button class="help-send-btn" onclick="sendHelpMessage()">➤</button>
        </div>
    </div>
    <script>
    // Chatbot functions
    function toggleHelpWindow() {
        var w = document.getElementById('helpWindow');
        if (w) w.classList.toggle('open');
    }
    
    function setHelpMode(mode) {
        document.querySelectorAll('.help-mode-btn').forEach(function(b) { b.classList.remove('active'); });
        var btn = document.getElementById(mode + 'ModeBtn');
        if (btn) btn.classList.add('active');
        document.getElementById('helpRagSelector').style.display = mode === 'rag' ? 'block' : 'none';
        document.getElementById('helpSupportBanner').style.display = mode === 'support' ? 'block' : 'none';
        window.helpMode = mode;
    }
    
    function sendHelpMessage() {
        var input = document.getElementById('helpInput');
        var msgs = document.getElementById('helpMessages');
        if (!input || !msgs) return;
        var msg = input.value.trim();
        if (!msg) return;
        
        // Add user message
        msgs.innerHTML += '<div class="help-message help-user"><div class="help-bubble-msg">' + msg + '</div></div>';
        input.value = '';
        
        // Add loading
        var lid = 'loading' + Date.now();
        msgs.innerHTML += '<div class="help-message help-bot" id="' + lid + '"><div class="help-bubble-msg">⏳ Réflexion...</div></div>';
        msgs.scrollTop = msgs.scrollHeight;
        
        // Call API
        fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg, mode: window.helpMode || 'chat'})
        })
        .then(function(r) { return r.json(); })
        .then(function(d) {
            var el = document.querySelector('#' + lid + ' .help-bubble-msg');
            if (el) el.textContent = d.response || 'Réponse reçue';
        })
        .catch(function() {
            var el = document.querySelector('#' + lid + ' .help-bubble-msg');
            if (el) el.textContent = '❌ Erreur de connexion';
        });
        msgs.scrollTop = msgs.scrollHeight;
    }
    
    window.helpMode = 'chat';
    </script>
'''

# Insert CSS before </style>
content = content.replace('    </style>', css + '\n    </style>')

# Insert HTML before </body>
content = content.replace('</body>', html + '\n</body>')

# Write back
with open('/opt/iafactory-rag-dz/apps/creative-studio/index.html', 'w') as f:
    f.write(content)

print('✅ Chatbot help integre dans creative-studio')
