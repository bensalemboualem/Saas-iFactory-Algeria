import { Link } from "react-router-dom";
import "./Onboarding.css";

export default function Onboarding() {
  return (
    <div className="onboarding-page">
      <header className="onboarding-hero">
        <p className="onboarding-kicker">Dzir IA • Démarrage rapide</p>
        <h1>Connecte tes sources, puis demande n’importe quoi.</h1>
        <p className="onboarding-subtitle">
          3 étapes simples pour obtenir des réponses sourcées et une mémoire organisée.
        </p>
      </header>

      <section className="onboarding-steps">
        <div className="step-card">
          <div className="step-number">1</div>
          <h2>Crée une collection</h2>
          <p>Regroupe tes thèmes : projets, clients, études, recherche, etc.</p>
          <Link className="btn-ghost" to="/collections">
            Créer une collection
          </Link>
        </div>
        <div className="step-card">
          <div className="step-number">2</div>
          <h2>Ajoute une source</h2>
          <p>URL, PDF ou texte. Dzir IA prépare les chunks pour la recherche.</p>
          <Link className="btn-ghost" to="/sources">
            Ajouter une source
          </Link>
        </div>
        <div className="step-card">
          <div className="step-number">3</div>
          <h2>Ask Dzir IA</h2>
          <p>Pose une question. Les réponses citent les sources.</p>
          <Link className="btn-ghost" to="/ask">
            Poser une question
          </Link>
        </div>
      </section>

      <section className="onboarding-grid">
        <div className="onboarding-panel">
          <h3>Local-first</h3>
          <p>Les données restent chez toi. Tu choisis le modèle (BYOK).</p>
        </div>
        <div className="onboarding-panel">
          <h3>FR / AR / DZ</h3>
          <p>Prêt pour un usage local et multilingue.</p>
        </div>
        <div className="onboarding-panel">
          <h3>Ask + Search</h3>
          <p>RAG + recherche classique, pour ne rien rater.</p>
        </div>
      </section>

      <section className="onboarding-cta">
        <div>
          <h2>Tu peux commencer en 2 minutes.</h2>
          <p>Crée une collection, ajoute un PDF, pose ta question.</p>
        </div>
        <div className="onboarding-actions">
          <Link className="btn-primary" to="/collections">
            Créer une collection
          </Link>
          <Link className="btn-ghost" to="/ask">
            Ask maintenant
          </Link>
        </div>
      </section>
    </div>
  );
}
