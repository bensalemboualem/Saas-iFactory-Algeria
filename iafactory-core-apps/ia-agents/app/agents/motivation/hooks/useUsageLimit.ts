'use client';

import { useState, useEffect } from 'react';
import { format, startOfDay } from 'date-fns';

const DAILY_LIMIT = parseInt(process.env.NEXT_PUBLIC_DAILY_MESSAGE_LIMIT || '10');

export function useUsageLimit() {
  const [messagesUsedToday, setMessagesUsedToday] = useState(0);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const today = format(new Date(), 'yyyy-MM-dd');
    const saved = localStorage.getItem('usage_limit_data');

    if (saved) {
      const data = JSON.parse(saved);

      if (data.date === today) {
        setMessagesUsedToday(data.count);
      } else {
        // New day, reset
        const newData = { date: today, count: 0 };
        localStorage.setItem('usage_limit_data', JSON.stringify(newData));
        setMessagesUsedToday(0);
      }
    } else {
      const newData = { date: today, count: 0 };
      localStorage.setItem('usage_limit_data', JSON.stringify(newData));
    }
  }, []);

  const incrementUsage = () => {
    const today = format(new Date(), 'yyyy-MM-dd');
    const newCount = messagesUsedToday + 1;

    const data = { date: today, count: newCount };
    localStorage.setItem('usage_limit_data', JSON.stringify(data));
    setMessagesUsedToday(newCount);

    if (newCount >= DAILY_LIMIT) {
      setShowModal(true);
    }
  };

  const canSendMessage = () => {
    return messagesUsedToday < DAILY_LIMIT;
  };

  const showLeadCapture = () => {
    setShowModal(true);
  };

  const hideModal = () => {
    setShowModal(false);
  };

  return {
    messagesUsedToday,
    dailyLimit: DAILY_LIMIT,
    canSendMessage,
    incrementUsage,
    showLeadCapture,
    hideModal,
    showModal,
  };
}
