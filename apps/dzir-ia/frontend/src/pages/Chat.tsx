import { Link } from "react-router-dom";
import DzirIAChat from "../components/dziria/DzirIAChat";
import "./Ask.css";

export default function Chat() {
  return (
    <div className="ask-page">
      <header className="ask-hero">
        <div>
          <p className="ask-kicker">Ask Dzir IA</p>
          <h1>Pose ta question, reçois des réponses sourcées.</h1>
          <p className="ask-subtitle">
            Dzir IA s’appuie sur tes sources (collections) et cite les passages utilisés.
          </p>
        </div>
        <div className="ask-hero-actions">
          <Link className="btn-primary" to="/onboarding">Connecter des sources</Link>
          <Link className="btn-ghost" to="/collections">Gérer les collections</Link>
        </div>
      </header>

      <div className="ask-layout">
        <section className="ask-chat">
          <DzirIAChat />
        </section>
        <aside className="ask-side">
          <div className="ask-card">
            <h3>Conseils</h3>
            <ul>
              <li>Précise le contexte et le but de ta question.</li>
              <li>Choisis une collection pour limiter le scope.</li>
              <li>Utilise “Search” si tu veux lister les chunks.</li>
            </ul>
          </div>
          <div className="ask-card">
            <h3>Modes</h3>
            <p>
              “Chat” = réponse avec citations. “Search” = résultats bruts.
            </p>
          </div>
          <div className="ask-card">
            <h3>Local‑first</h3>
            <p>Tu peux activer BYOK pour contrôler les coûts LLM.</p>
          </div>
        </aside>
      </div>
    </div>
  );
}
