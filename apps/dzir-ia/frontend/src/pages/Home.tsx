import { Link } from 'react-router-dom';
import { useState } from 'react';
import CaptureModal from '../components/CaptureModal';
import './Home.css';

export default function Home() {
  const [captureOpen, setCaptureOpen] = useState(false);

  return (
    <div className="home-page">
      <header className="home-hero">
        <div className="home-hero-text">
          <p className="home-kicker">Dzir IA • Second Brain</p>
          <h1>Ton assistant personnel, alimenté par tout ce que tu fais.</h1>
          <p className="home-subtitle">
            Capture automatique, recherche intelligente, et réponses sourcées. Plus rapide,
            plus clair, plus “toi”.
          </p>
          <div className="home-actions">
            <Link className="btn-primary" to="/ask">Ask Dzir IA</Link>
            <button className="btn-ghost" onClick={() => setCaptureOpen(true)}>
              Capturer maintenant
            </button>
          </div>
          <div className="home-badges">
            <span>Local-first</span>
            <span>BYOK</span>
            <span>FR / AR</span>
          </div>
          <div className="home-links">
            <Link to="/onboarding">Démarrer en 2 minutes</Link>
            <Link to="/sources">Voir les sources</Link>
            <Link to="/landing">Voir la landing</Link>
          </div>
        </div>
        <div className="home-hero-card">
          <div className="hero-card-title">Aujourd’hui</div>
          <ul className="hero-card-list">
            <li>Auto-capture activée</li>
            <li>12 nouveaux éléments</li>
            <li>3 collections actives</li>
          </ul>
          <div className="hero-card-cta">
            <Link className="btn-primary" to="/sources">Organiser mes sources</Link>
          </div>
        </div>
      </header>

      <section className="home-grid">
        <div className="home-panel">
          <h2>Auto-capture</h2>
          <p>Pages, PDFs, notes, emails… tout arrive sans effort.</p>
          <div className="panel-actions">
            <button className="btn-ghost" onClick={() => setCaptureOpen(true)}>
              Ajouter une source
            </button>
          </div>
        </div>
        <div className="home-panel">
          <h2>Ask avec citations</h2>
          <p>Pose une question. Dzir IA répond avec les sources.</p>
          <div className="panel-actions">
            <Link className="btn-ghost" to="/ask">Poser une question</Link>
          </div>
        </div>
        <div className="home-panel">
          <h2>Recherche instantanée</h2>
          <p>Retrouve un document ou un passage en quelques secondes.</p>
          <div className="panel-actions">
            <Link className="btn-ghost" to="/search">Rechercher</Link>
          </div>
        </div>
        <div className="home-panel">
          <h2>Timeline</h2>
          <p>Visualise l’activité et l’historique de tes captures.</p>
          <div className="panel-actions">
            <Link className="btn-ghost" to="/timeline">Voir la timeline</Link>
          </div>
        </div>
      </section>

      <section className="home-cta">
        <div>
          <h2>Connecte tes sources</h2>
          <p>
            Commence par 1 collection, puis ajoute tes PDFs, pages web et notes.
          </p>
        </div>
        <div className="home-cta-actions">
          <Link className="btn-primary" to="/onboarding">Onboarding</Link>
          <button className="btn-ghost" onClick={() => setCaptureOpen(true)}>
            Capture rapide
          </button>
        </div>
      </section>

      <CaptureModal isOpen={captureOpen} onClose={() => setCaptureOpen(false)} />
    </div>
  );
}
