import { Link } from 'react-router-dom';
import './Landing.css';

export default function Landing() {
  return (
    <div className="landing-page">
      <header className="landing-hero">
        <div className="landing-hero-text">
          <p className="landing-kicker">Dzir IA • Second Brain</p>
          <h1>Auto‑capture + Ask AI. Ta mémoire augmentée, locale et privée.</h1>
          <p className="landing-subtitle">
            Dzir IA unifie tes sources (web, PDF, notes) et te répond avec citations.
            Local‑first, BYOK, FR/AR.
          </p>
          <div className="landing-actions">
            <Link className="btn-primary" to="/onboarding">Démarrer</Link>
            <Link className="btn-ghost" to="/">Ouvrir l’app</Link>
          </div>
          <div className="landing-badges">
            <span>Local-first</span>
            <span>BYOK</span>
            <span>FR / AR</span>
          </div>
        </div>
        <div className="landing-hero-card">
          <div className="hero-card-title">Ce que Dzir IA fait pour toi</div>
          <ul className="hero-card-list">
            <li>Capture automatique des sources</li>
            <li>Recherche sémantique + Ask</li>
            <li>Réponses sourcées</li>
            <li>Timeline d’activité</li>
          </ul>
          <div className="hero-card-cta">
            <Link className="btn-primary" to="/onboarding">Connecter mes sources</Link>
          </div>
        </div>
      </header>

      <section className="landing-steps">
        <div className="step-card">
          <div className="step-number">1</div>
          <h2>Connecte</h2>
          <p>Crée une collection et ajoute tes sources clés.</p>
        </div>
        <div className="step-card">
          <div className="step-number">2</div>
          <h2>Capture</h2>
          <p>URLs, PDFs, notes… tout est indexé pour toi.</p>
        </div>
        <div className="step-card">
          <div className="step-number">3</div>
          <h2>Ask</h2>
          <p>Pose une question, obtient des réponses citant tes sources.</p>
        </div>
      </section>

      <section className="landing-grid">
        <div className="landing-panel">
          <h3>Local‑first</h3>
          <p>Tu gardes le contrôle. Les données restent locales.</p>
        </div>
        <div className="landing-panel">
          <h3>BYOK</h3>
          <p>Utilise ta propre clé LLM pour réduire les coûts.</p>
        </div>
        <div className="landing-panel">
          <h3>Multi‑langue</h3>
          <p>Conçu pour FR/AR et usage DZ.</p>
        </div>
        <div className="landing-panel">
          <h3>Sources fiables</h3>
          <p>Chaque réponse cite les documents utilisés.</p>
        </div>
      </section>

      <section className="landing-pricing">
        <h2>Pricing</h2>
        <div className="pricing-grid">
          <div className="pricing-card">
            <h3>Free</h3>
            <p className="price">0 DA</p>
            <ul>
              <li>Collections illimitées</li>
              <li>Capture manuelle</li>
              <li>Ask (limité)</li>
            </ul>
            <Link className="btn-ghost" to="/onboarding">Commencer</Link>
          </div>
          <div className="pricing-card featured">
            <h3>Pro</h3>
            <p className="price">— DA</p>
            <ul>
              <li>Auto‑capture</li>
              <li>Ask illimité</li>
              <li>Timeline avancée</li>
            </ul>
            <Link className="btn-primary" to="/onboarding">Essayer Pro</Link>
          </div>
          <div className="pricing-card">
            <h3>BYOK</h3>
            <p className="price">Pay‑as‑you‑go</p>
            <ul>
              <li>Utilise ta clé LLM</li>
              <li>Coûts maîtrisés</li>
              <li>Modes locaux</li>
            </ul>
            <Link className="btn-ghost" to="/onboarding">Configurer</Link>
          </div>
        </div>
      </section>

      <section className="landing-cta">
        <div>
          <h2>Prêt à démarrer ?</h2>
          <p>Connecte tes sources en 2 minutes.</p>
        </div>
        <div className="landing-actions">
          <Link className="btn-primary" to="/onboarding">Démarrer</Link>
          <Link className="btn-ghost" to="/">Ouvrir l’app</Link>
        </div>
      </section>
    </div>
  );
}
