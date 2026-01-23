'use client';

import { useEffect, useState } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export default function PWAInstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [showInstallPrompt, setShowInstallPrompt] = useState(false);
  const [isIOS, setIsIOS] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
      return;
    }

    // Check if iOS
    const iOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    setIsIOS(iOS);

    // Listen for beforeinstallprompt event (Android/Chrome)
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);

      // Show install prompt after 5 seconds
      setTimeout(() => {
        setShowInstallPrompt(true);
      }, 5000);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    // Check if user dismissed prompt before
    const dismissed = localStorage.getItem('pwa-install-dismissed');
    if (dismissed) {
      const dismissedTime = parseInt(dismissed, 10);
      const daysSinceDismissed = (Date.now() - dismissedTime) / (1000 * 60 * 60 * 24);

      // Show again after 7 days
      if (daysSinceDismissed < 7) {
        setShowInstallPrompt(false);
      }
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;

    if (outcome === 'accepted') {
      console.log('PWA installed');
      setIsInstalled(true);
    }

    setDeferredPrompt(null);
    setShowInstallPrompt(false);
  };

  const handleDismiss = () => {
    setShowInstallPrompt(false);
    localStorage.setItem('pwa-install-dismissed', Date.now().toString());
  };

  // Don't show if already installed
  if (isInstalled) return null;

  // iOS Install Instructions
  if (isIOS && showInstallPrompt) {
    return (
      <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-r from-primary to-secondary text-white p-4 shadow-lg z-50 animate-slide-up">
        <div className="container-app">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <span className="text-2xl">📱</span>
                <h3 className="font-bold text-lg">Installer CAN 2025</h3>
              </div>
              <p className="text-sm text-white/90 mb-3">
                Pour installer l'app sur votre iPhone:
              </p>
              <ol className="text-sm text-white/90 space-y-1 list-decimal list-inside">
                <li>Appuyez sur le bouton Partager <span className="inline-block">⎋</span></li>
                <li>Sélectionnez "Sur l'écran d'accueil"</li>
                <li>Confirmez l'installation</li>
              </ol>
            </div>
            <button
              onClick={handleDismiss}
              className="ml-4 text-white/80 hover:text-white text-2xl leading-none"
              aria-label="Fermer"
            >
              ×
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Android/Chrome Install Prompt
  if (deferredPrompt && showInstallPrompt) {
    return (
      <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-r from-primary to-secondary text-white p-4 shadow-lg z-50 animate-slide-up">
        <div className="container-app">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3 flex-1">
              <span className="text-3xl">📱</span>
              <div>
                <h3 className="font-bold text-lg">Installer CAN 2025</h3>
                <p className="text-sm text-white/90">
                  Ajoutez l'app à votre écran d'accueil pour un accès rapide!
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2 ml-4">
              <button
                onClick={handleInstallClick}
                className="bg-white text-primary font-semibold px-6 py-2 rounded-lg hover:bg-white/90 transition-colors"
              >
                Installer
              </button>
              <button
                onClick={handleDismiss}
                className="text-white/80 hover:text-white px-3 py-2"
                aria-label="Plus tard"
              >
                Plus tard
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
}
