'use client';

import { useEffect, useState } from 'react';

export default function NotificationPermission() {
  const [showPrompt, setShowPrompt] = useState(false);
  const [permission, setPermission] = useState<NotificationPermission>('default');

  useEffect(() => {
    // Check current permission status
    if ('Notification' in window) {
      setPermission(Notification.permission);

      // Show prompt after 10 seconds if permission not granted
      if (Notification.permission === 'default') {
        const timer = setTimeout(() => {
          // Check if user dismissed before
          const dismissed = localStorage.getItem('notifications-dismissed');
          if (!dismissed || Date.now() - parseInt(dismissed, 10) > 7 * 24 * 60 * 60 * 1000) {
            setShowPrompt(true);
          }
        }, 10000);

        return () => clearTimeout(timer);
      }
    }
  }, []);

  const handleRequestPermission = async () => {
    if (!('Notification' in window)) {
      alert('Votre navigateur ne supporte pas les notifications');
      return;
    }

    try {
      const permission = await Notification.requestPermission();
      setPermission(permission);

      if (permission === 'granted') {
        console.log('Notification permission granted');
        setShowPrompt(false);

        // Subscribe to push notifications
        await subscribeToPushNotifications();

        // Show success notification
        new Notification('CAN 2025 - Notifications activées! 🎉', {
          body: 'Vous recevrez des alertes avant les matchs de l\'Algérie',
          icon: '/icon-192x192.png',
          badge: '/icon-192x192.png',
          tag: 'permission-granted',
        });
      } else {
        console.log('Notification permission denied');
        setShowPrompt(false);
      }
    } catch (error) {
      console.error('Error requesting notification permission:', error);
    }
  };

  const subscribeToPushNotifications = async () => {
    try {
      // Register service worker
      const registration = await navigator.serviceWorker.ready;

      // Check if already subscribed
      const existingSubscription = await registration.pushManager.getSubscription();
      if (existingSubscription) {
        console.log('Already subscribed to push notifications');
        return;
      }

      // VAPID public key (to be generated)
      // For now, just log that we would subscribe
      console.log('Would subscribe to push notifications here with VAPID key');

      // In production, you would:
      // 1. Generate VAPID keys (npm run generate-vapid)
      // 2. Store public key in env
      // 3. Subscribe user
      // 4. Send subscription to backend

      /*
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY!)
      });

      // Send subscription to your backend
      await fetch('/api/push-subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(subscription)
      });
      */
    } catch (error) {
      console.error('Error subscribing to push notifications:', error);
    }
  };

  const handleDismiss = () => {
    setShowPrompt(false);
    localStorage.setItem('notifications-dismissed', Date.now().toString());
  };

  if (!showPrompt || permission !== 'default') return null;

  return (
    <div className="fixed bottom-20 left-4 right-4 md:left-auto md:right-4 md:w-96 bg-white dark:bg-slate-800 rounded-xl shadow-2xl p-6 z-50 border-2 border-primary animate-slide-up">
      <div className="flex items-start space-x-3 mb-4">
        <span className="text-4xl">🔔</span>
        <div className="flex-1">
          <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
            Activer les notifications?
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Recevez des alertes avant les matchs de l'Algérie et les moments clés de la CAN 2025
          </p>
        </div>
      </div>

      <div className="space-y-2 mb-4 text-sm text-slate-600 dark:text-slate-400">
        <div className="flex items-center space-x-2">
          <span className="text-primary">✓</span>
          <span>15 min avant chaque match de l'Algérie 🇩🇿</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-primary">✓</span>
          <span>Résultats en temps réel</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-primary">✓</span>
          <span>Qualifications et phases finales</span>
        </div>
      </div>

      <div className="flex space-x-2">
        <button
          onClick={handleRequestPermission}
          className="flex-1 bg-gradient-to-r from-primary to-secondary text-white font-semibold py-3 px-4 rounded-lg hover:opacity-90 transition-opacity"
        >
          Activer
        </button>
        <button
          onClick={handleDismiss}
          className="px-4 py-3 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
        >
          Plus tard
        </button>
      </div>
    </div>
  );
}
