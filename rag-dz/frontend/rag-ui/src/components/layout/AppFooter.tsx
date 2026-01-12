import React from 'react';

export function AppFooter() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="iaf-footer">
      <div className="iaf-footer-grid">
        {/* Column 1: IAFactory Info + Social Links */}
        <div className="iaf-footer-col">
          <h4>IAFactory Algeria</h4>
          <p>Plateforme IA souveraine pour le marche algerien.</p>
          <p style={{ marginTop: "0.5rem" }}>
            <i className="fas fa-map-marker-alt"></i> Alger, Algerie
          </p>
          {/* Social Links */}
          <div className="iaf-social-links">
            <a href="#" className="iaf-social-link" aria-label="TikTok">
              <i className="fab fa-tiktok"></i>
            </a>
            <a href="#" className="iaf-social-link" aria-label="YouTube">
              <i className="fab fa-youtube"></i>
            </a>
            <a href="#" className="iaf-social-link" aria-label="Instagram">
              <i className="fab fa-instagram"></i>
            </a>
            <a href="#" className="iaf-social-link" aria-label="Facebook">
              <i className="fab fa-facebook-f"></i>
            </a>
            <a href="#" className="iaf-social-link" aria-label="LinkedIn">
              <i className="fab fa-linkedin-in"></i>
            </a>
            <a href="#" className="iaf-social-link" aria-label="X">
              <i className="fab fa-x-twitter"></i>
            </a>
            <a href="https://github.com/iafactory" className="iaf-social-link" aria-label="GitHub">
              <i className="fab fa-github"></i>
            </a>
            <a href="#" className="iaf-social-link" aria-label="Discord">
              <i className="fab fa-discord"></i>
            </a>
          </div>
        </div>

        {/* Column 2: Produits */}
        <div className="iaf-footer-col">
          <h4>Produits</h4>
          <ul>
            <li><a href="https://www.iafactoryalgeria.com/apps.html">Applications</a></li>
            <li><a href="https://video.iafactoryalgeria.com">Studio Video</a></li>
            <li><a href="https://voice.iafactoryalgeria.com">Voice Assistant</a></li>
          </ul>
        </div>

        {/* Column 3: Ressources */}
        <div className="iaf-footer-col">
          <h4>Ressources</h4>
          <ul>
            <li><a href="https://www.iafactoryalgeria.com/docs">Documentation</a></li>
            <li><a href="https://api.iafactoryalgeria.com/docs">API Reference</a></li>
            <li><a href="https://www.iafactoryalgeria.com/blog">Blog</a></li>
          </ul>
        </div>

        {/* Column 4: Entreprise */}
        <div className="iaf-footer-col">
          <h4>Entreprise</h4>
          <ul>
            <li><a href="https://www.iafactoryalgeria.com/about">A propos</a></li>
            <li><a href="https://www.iafactoryalgeria.com/contact">Contact</a></li>
            <li><a href="https://www.iafactoryalgeria.com/careers">Carrieres</a></li>
          </ul>
        </div>

        {/* Column 5: Legal */}
        <div className="iaf-footer-col">
          <h4>Legal</h4>
          <ul>
            <li><a href="https://www.iafactoryalgeria.com/privacy">Confidentialite</a></li>
            <li><a href="https://www.iafactoryalgeria.com/terms">Conditions</a></li>
            <li><a href="https://www.iafactoryalgeria.com/legal">Mentions legales</a></li>
          </ul>
        </div>
      </div>

      {/* Footer Bottom */}
      <div className="iaf-footer-bottom">
        &copy; {currentYear} IAFactory Algeria. Tous droits reserves.
      </div>
    </footer>
  );
}

export default AppFooter;
