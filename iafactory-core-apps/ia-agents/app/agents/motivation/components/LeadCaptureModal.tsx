'use client';

import { useState } from 'react';

interface LeadCaptureModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function LeadCaptureModal({ isOpen, onClose }: LeadCaptureModalProps) {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // TODO: Send to backend/email service
    console.log('Lead captured:', email);

    // Save to localStorage for now
    localStorage.setItem('user_email', email);

    setSubmitted(true);

    setTimeout(() => {
      onClose();
      setSubmitted(false);
      setEmail('');
    }, 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="card max-w-lg w-full animate-slide-up">
        {!submitted ? (
          <>
            {/* Header */}
            <div className="text-center mb-6">
              <div className="text-5xl mb-3">💪</div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
                Continue avec Amine!
              </h2>
              <p className="text-slate-600 dark:text-slate-400">
                Tu as atteint la limite gratuite de 10 messages/jour.
              </p>
            </div>

            {/* Benefits */}
            <div className="bg-gradient-to-br from-primary/10 to-emerald-500/10 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-slate-900 dark:text-white mb-3">
                IA Motivation Premium - 2000 DA/mois
              </h3>
              <ul className="space-y-2 text-sm text-slate-700 dark:text-slate-300">
                <li className="flex items-start space-x-2">
                  <span className="text-primary">✓</span>
                  <span>Messages illimités avec Amine</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-primary">✓</span>
                  <span>Tous les achievements débloqués</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-primary">✓</span>
                  <span>Export historique conversations</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-primary">✓</span>
                  <span>Objectifs personnalisés & suivi détaillé</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-primary">✓</span>
                  <span>Support prioritaire</span>
                </li>
              </ul>
            </div>

            {/* Email Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  Entre ton email pour recevoir plus d'infos:
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="ton@email.com"
                  required
                  className="input-field"
                />
              </div>

              <button type="submit" className="btn-primary w-full">
                Passer à Premium 🚀
              </button>

              <button
                type="button"
                onClick={onClose}
                className="w-full py-2 text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
              >
                Peut-être plus tard
              </button>
            </form>

            {/* Trust */}
            <div className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-800 text-center">
              <p className="text-xs text-slate-500 dark:text-slate-400">
                🔒 Tes données sont sécurisées. Annule à tout moment.
              </p>
            </div>
          </>
        ) : (
          <div className="text-center py-8">
            <div className="text-6xl mb-4">🎉</div>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
              Merci!
            </h3>
            <p className="text-slate-600 dark:text-slate-400">
              On va te contacter très bientôt pour activer Premium!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
