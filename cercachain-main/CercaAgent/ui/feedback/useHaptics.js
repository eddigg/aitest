import { useFeedback } from './FeedbackManager';

export const useHaptics = () => {
  const { settings } = useFeedback();

  const isVibrationSupported = () => {
    return 'vibrate' in navigator || 'mozVibrate' in navigator;
  };

  const vibrate = (pattern) => {
    if (!settings.haptic || !isVibrationSupported()) return false;

    try {
      // Normalize pattern to array if single number provided
      const vibrationPattern = Array.isArray(pattern) ? pattern : [pattern];
      navigator.vibrate(vibrationPattern);
      return true;
    } catch (error) {
      console.error('Haptic feedback failed:', error);
      return false;
    }
  };

  // Predefined vibration patterns
  const patterns = {
    success: [100],
    error: [100, 100, 100],
    warning: [200, 100, 200],
    notification: [50],
    processing: [50, 100, 50]
  };

  const hapticFeedback = {
    success: () => vibrate(patterns.success),
    error: () => vibrate(patterns.error),
    warning: () => vibrate(patterns.warning),
    notification: () => vibrate(patterns.notification),
    processing: () => vibrate(patterns.processing),
    custom: (pattern) => vibrate(pattern)
  };

  return {
    isSupported: isVibrationSupported(),
    vibrate,
    patterns,
    ...hapticFeedback
  };
};