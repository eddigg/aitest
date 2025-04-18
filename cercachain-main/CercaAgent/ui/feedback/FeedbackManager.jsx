import React, { createContext, useContext, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Lottie from 'react-lottie';

// Create feedback context
const FeedbackContext = createContext();

// Custom hook for using feedback
export const useFeedback = () => {
  const context = useContext(FeedbackContext);
  if (!context) {
    throw new Error('useFeedback must be used within a FeedbackProvider');
  }
  return context;
};

// Feedback settings interface
const defaultSettings = {
  visual: true,
  audio: true,
  haptic: true,
  toastPosition: 'bottom-right',
  toastAutoClose: 3000,
};

export const FeedbackProvider = ({ children }) => {
  const [settings, setSettings] = useState(defaultSettings);

  // Visual feedback using toast
  const showVisualFeedback = (message, type = 'info') => {
    if (!settings.visual) return;
    toast[type](message, {
      position: settings.toastPosition,
      autoClose: settings.toastAutoClose,
    });
  };

  // Haptic feedback using Vibration API
  const triggerHapticFeedback = (pattern = [200]) => {
    if (!settings.haptic || !navigator.vibrate) return;
    navigator.vibrate(pattern);
  };

  // Audio feedback using Web Audio API
  const playAudioFeedback = async (text) => {
    if (!settings.audio) return;
    try {
      const response = await fetch('/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      const audioBlob = await response.blob();
      const audio = new Audio(URL.createObjectURL(audioBlob));
      await audio.play();
    } catch (error) {
      console.error('Audio feedback failed:', error);
    }
  };

  // Combined feedback function
  const provideFeedback = async ({
    message,
    type = 'info',
    hapticPattern = [200],
    playAudio = false,
  }) => {
    showVisualFeedback(message, type);
    triggerHapticFeedback(hapticPattern);
    if (playAudio) await playAudioFeedback(message);
  };

  const value = {
    settings,
    setSettings,
    showVisualFeedback,
    triggerHapticFeedback,
    playAudioFeedback,
    provideFeedback,
  };

  return (
    <FeedbackContext.Provider value={value}>
      {children}
      <ToastContainer />
    </FeedbackContext.Provider>
  );
};