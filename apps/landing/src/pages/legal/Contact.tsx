import { useState } from 'react';
import { useTheme } from '../../hooks';

export default function Contact() {
  const { colors, accent } = useTheme();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Intégrer avec un backend
    console.log('Form submitted:', formData);
    setSubmitted(true);
  };

  const inputStyle = {
    width: '100%',
    padding: '14px 16px',
    borderRadius: '8px',
    border: `1px solid ${colors.borderColor}`,
    background: colors.bgSecondary,
    color: colors.textPrimary,
    fontSize: '16px',
    outline: 'none',
    transition: 'border-color 0.2s',
  };

  const labelStyle = {
    display: 'block',
    color: colors.textPrimary,
    fontSize: '14px',
    fontWeight: 500,
    marginBottom: '8px',
  };

  const cardStyle = {
    background: colors.bgSecondary,
    borderRadius: '16px',
    padding: '32px',
    border: `1px solid ${colors.borderColor}`,
  };

  return (
    <main
      style={{
        minHeight: '100vh',
        background: colors.bgPrimary,
        padding: '120px 24px 60px',
      }}
    >
      <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <h1
            style={{
              color: colors.textPrimary,
              fontSize: '42px',
              fontWeight: 700,
              marginBottom: '12px',
            }}
          >
            Contactez-nous
          </h1>
          <p style={{ color: colors.textMuted, fontSize: '18px' }}>
            Une question ? Un projet ? Nous sommes là pour vous aider.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px' }}>
          {/* Contact Info */}
          <div>
            <div style={{ ...cardStyle, marginBottom: '24px' }}>
              <h2 style={{ color: colors.textPrimary, fontSize: '20px', fontWeight: 600, marginBottom: '24px' }}>
                Informations de contact
              </h2>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '12px',
                    background: `${accent.primary}20`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '24px',
                    flexShrink: 0,
                  }}>
                    📧
                  </div>
                  <div>
                    <h3 style={{ color: colors.textPrimary, fontSize: '16px', fontWeight: 600, marginBottom: '4px' }}>Email</h3>
                    <a href="mailto:contact@iafactory.ai" style={{ color: accent.primary, textDecoration: 'none' }}>
                      contact@iafactory.ai
                    </a>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '12px',
                    background: `${accent.primary}20`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '24px',
                    flexShrink: 0,
                  }}>
                    🛠️
                  </div>
                  <div>
                    <h3 style={{ color: colors.textPrimary, fontSize: '16px', fontWeight: 600, marginBottom: '4px' }}>Support technique</h3>
                    <a href="mailto:support@iafactory.ai" style={{ color: accent.primary, textDecoration: 'none' }}>
                      support@iafactory.ai
                    </a>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '12px',
                    background: `${accent.primary}20`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '24px',
                    flexShrink: 0,
                  }}>
                    📍
                  </div>
                  <div>
                    <h3 style={{ color: colors.textPrimary, fontSize: '16px', fontWeight: 600, marginBottom: '4px' }}>Adresse</h3>
                    <p style={{ color: colors.textMuted }}>Alger, Algérie</p>
                  </div>
                </div>
              </div>
            </div>

            <div style={cardStyle}>
              <h2 style={{ color: colors.textPrimary, fontSize: '20px', fontWeight: 600, marginBottom: '16px' }}>
                Horaires de support
              </h2>
              <ul style={{ color: colors.textSecondary, listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span>Dimanche - Jeudi</span>
                  <span style={{ color: colors.textPrimary }}>9h00 - 18h00</span>
                </li>
                <li style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span>Vendredi</span>
                  <span style={{ color: colors.textMuted }}>Fermé</span>
                </li>
                <li style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Samedi</span>
                  <span style={{ color: colors.textPrimary }}>10h00 - 14h00</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Contact Form */}
          <div style={cardStyle}>
            {submitted ? (
              <div style={{ textAlign: 'center', padding: '40px 0' }}>
                <div style={{ fontSize: '64px', marginBottom: '16px' }}>✅</div>
                <h2 style={{ color: colors.textPrimary, fontSize: '24px', fontWeight: 600, marginBottom: '8px' }}>
                  Message envoyé !
                </h2>
                <p style={{ color: colors.textMuted }}>
                  Nous vous répondrons dans les plus brefs délais.
                </p>
              </div>
            ) : (
              <>
                <h2 style={{ color: colors.textPrimary, fontSize: '20px', fontWeight: 600, marginBottom: '24px' }}>
                  Envoyez-nous un message
                </h2>
                <form onSubmit={handleSubmit}>
                  <div style={{ marginBottom: '20px' }}>
                    <label style={labelStyle}>Nom complet</label>
                    <input
                      type="text"
                      required
                      style={inputStyle}
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      placeholder="Votre nom"
                    />
                  </div>
                  <div style={{ marginBottom: '20px' }}>
                    <label style={labelStyle}>Email</label>
                    <input
                      type="email"
                      required
                      style={inputStyle}
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      placeholder="votre@email.com"
                    />
                  </div>
                  <div style={{ marginBottom: '20px' }}>
                    <label style={labelStyle}>Sujet</label>
                    <select
                      style={inputStyle}
                      value={formData.subject}
                      onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                    >
                      <option value="">Sélectionnez un sujet</option>
                      <option value="general">Question générale</option>
                      <option value="support">Support technique</option>
                      <option value="billing">Facturation</option>
                      <option value="partnership">Partenariat</option>
                      <option value="b2b">Offre B2B</option>
                    </select>
                  </div>
                  <div style={{ marginBottom: '24px' }}>
                    <label style={labelStyle}>Message</label>
                    <textarea
                      required
                      rows={5}
                      style={{ ...inputStyle, resize: 'vertical' }}
                      value={formData.message}
                      onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                      placeholder="Décrivez votre demande..."
                    />
                  </div>
                  <button
                    type="submit"
                    style={{
                      width: '100%',
                      padding: '14px',
                      borderRadius: '8px',
                      border: 'none',
                      background: accent.primary,
                      color: '#fff',
                      fontSize: '16px',
                      fontWeight: 600,
                      cursor: 'pointer',
                    }}
                  >
                    Envoyer le message
                  </button>
                </form>
              </>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
