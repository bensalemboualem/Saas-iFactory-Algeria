#!/usr/bin/env python3
import re

LANDING = "/opt/iafactory-rag-dz/apps/landing/index.html"

# Read current content
with open(LANDING, "r", encoding="utf-8") as f:
    content = f.read()

print("Step 1: Creating AI Agents section...")
agents_html = '''
        <!-- AI AGENTS SECTION -->
        <section id="agents" class="section">
            <h2 class="section-title">🤖 18 AI Agents - Production Ready</h2>
            <p class="section-description">Agents IA autonomes et spécialisés pour automatiser vos tâches business, développement et analyses.</p>
            <div class="agents-grid">
                <article class="agent-card" data-category="business" data-audience="user">
                    <h5>💼 AI Consultant</h5>
                    <div class="badge">Business</div>
                    <p>Expert business consulting avec Google Gemini AI</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9101', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="business" data-audience="user">
                    <h5>🎧 Customer Support</h5>
                    <div class="badge">Business</div>
                    <p>Support client intelligent 24/7</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9102', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="business" data-audience="dev">
                    <h5>📊 Data Analysis</h5>
                    <div class="badge">Business</div>
                    <p>Analyse de données avancée avec visualisations</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9103', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="finance" data-audience="user">
                    <h5>💰 XAI Finance</h5>
                    <div class="badge">Finance</div>
                    <p>Analyse financière avec IA explicable</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9104', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="business" data-audience="user">
                    <h5>📅 Meeting Agent</h5>
                    <div class="badge">Business</div>
                    <p>Assistant de réunions avec transcription</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9105', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="business" data-audience="user">
                    <h5>📰 Journalist</h5>
                    <div class="badge">Business</div>
                    <p>Rédaction d'articles professionnels</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9106', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="developer" data-audience="dev">
                    <h5>🕷️ Web Scraping</h5>
                    <div class="badge">Developer</div>
                    <p>Extraction intelligente de données web</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9107', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="business" data-audience="user">
                    <h5>🚀 Product Launch</h5>
                    <div class="badge">Business</div>
                    <p>Planification de lancements produits</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9108', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="ia" data-audience="dev">
                    <h5>📚 Local RAG</h5>
                    <div class="badge">IA</div>
                    <p>RAG local avec Ollama et Qdrant</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9109', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="ia" data-audience="dev">
                    <h5>☁️ RAG as a Service</h5>
                    <div class="badge">IA</div>
                    <p>RAG service cloud multi-modèles</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9110', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="ia" data-audience="dev">
                    <h5>🤖 Agentic RAG</h5>
                    <div class="badge">IA</div>
                    <p>RAG avec agents autonomes</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9111', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="ia" data-audience="dev">
                    <h5>🧠 Autonomous RAG</h5>
                    <div class="badge">IA</div>
                    <p>RAG autonome auto-optimisé</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9112', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="ia" data-audience="dev">
                    <h5>🔍 Hybrid Search RAG</h5>
                    <div class="badge">IA</div>
                    <p>RAG avec recherche hybride</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9113', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="finance" data-audience="user">
                    <h5>💼 Investment Agent</h5>
                    <div class="badge">Finance</div>
                    <p>Conseil en investissement intelligent</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9114', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="finance" data-audience="user">
                    <h5>💳 Financial Coach</h5>
                    <div class="badge">Finance</div>
                    <p>Coach financier personnel IA</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9115', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="finance" data-audience="user">
                    <h5>📈 Startup Trends</h5>
                    <div class="badge">Finance</div>
                    <p>Analyse tendances startups</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9116', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="developer" data-audience="dev">
                    <h5>🏗️ System Architect</h5>
                    <div class="badge">Developer</div>
                    <p>Architecture système avec DeepSeek R1</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9117', '_blank')">Ouvrir</button>
                </article>
                <article class="agent-card" data-category="business" data-audience="dev">
                    <h5>🔬 Deep Research</h5>
                    <div class="badge">Business</div>
                    <p>Recherche approfondie multi-sources</p>
                    <button type="button" class="btn-round btn-primary" onclick="window.open('https://iafactoryalgeria.com/agents/9118', '_blank')">Ouvrir</button>
                </article>
            </div>
        </section>

'''

# Step 1: Insert agents section BEFORE <!-- APPS -->
if "<!-- APPS -->" in content:
    content = content.replace("        <!-- APPS -->", agents_html + "        <!-- APPS -->")
    print("✓ Agents section added")
else:
    print("✗ Could not find <!-- APPS --> marker")

print("\nStep 2: Removing port numbers from buttons...")
content = re.sub(r'(Ouvrir|Open)\s*:\s*\d{4,5}', r'\1', content)
print("✓ Port numbers removed")

print("\nStep 3: Adding 3D effect CSS...")
css_3d = '''
        /* ========== EFFET 3D CARTES ========== */
        .app-card, .agent-card {
            transform-style: preserve-3d;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .app-card:hover, .agent-card:hover {
            transform: translateY(-12px) rotateX(5deg) scale(1.02);
            box-shadow:
                0 25px 50px -12px rgba(0, 166, 81, 0.25),
                0 0 0 1px rgba(0, 166, 81, 0.1),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
        }

        [data-theme="light"] .app-card:hover,
        [data-theme="light"] .agent-card:hover {
            box-shadow:
                0 25px 50px -12px rgba(0, 166, 81, 0.15),
                0 0 0 1px rgba(0, 166, 81, 0.1),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.8);
        }

        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 24px;
            margin-top: 32px;
        }

        .agent-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            position: relative;
            overflow: hidden;
        }

        .agent-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), #00d66a);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .agent-card:hover::before {
            opacity: 1;
        }
'''

content = content.replace("    </style>", css_3d + "\n    </style>")
print("✓ 3D CSS added")

print("\nStep 4: Adding Dev/User toggle JavaScript...")
js_toggle = '''
        // ========== TOGGLE DEV/USER FUNCTIONALITY ==========
        const profileButtons = document.querySelectorAll('.profile-btn');
        let currentAudience = 'user';

        profileButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                profileButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                if (this.textContent.toLowerCase().includes('dev')) {
                    currentAudience = 'dev';
                } else {
                    currentAudience = 'user';
                }

                filterByAudience(currentAudience);
            });
        });

        function filterByAudience(audience) {
            const allCards = document.querySelectorAll('[data-audience]');

            allCards.forEach(card => {
                const cardAudience = card.getAttribute('data-audience');

                if (cardAudience === audience || cardAudience === 'both') {
                    card.style.display = '';
                    card.style.animation = 'fadeInUp 0.4s ease forwards';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(styleSheet);

        filterByAudience(currentAudience);
'''

last_script_pos = content.rfind("</script>")
if last_script_pos > 0:
    content = content[:last_script_pos] + js_toggle + "\n" + content[last_script_pos:]
    print("✓ Toggle JavaScript added")
else:
    print("✗ Could not find </script> tag")

print("\nStep 5: Verifying footer and chatbot are preserved...")
if "<footer" in content:
    print("✓ Footer preserved")
else:
    print("✗ WARNING: Footer missing!")

if "cb-help" in content or "chatbot" in content.lower():
    print("✓ Chatbot help preserved")
else:
    print("✗ WARNING: Chatbot might be missing!")

with open(LANDING, "w", encoding="utf-8") as f:
    f.write(content)

print("\n" + "="*60)
print("✓ Landing page updated successfully!")
print("="*60)
