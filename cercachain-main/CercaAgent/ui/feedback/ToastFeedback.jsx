import React from 'react';
import { useFeedback } from './FeedbackManager';

export const ToastFeedback = ({ message, type = 'info', haptic = true, audio = false }) => {
  const { provideFeedback } = useFeedback();

  React.useEffect(() => {
    provideFeedback({
      message,
      type,
      hapticPattern: haptic ? [200] : [],
      playAudio: audio,
    });
  }, [message, type, haptic, audio, provideFeedback]);

  return null; // This is a utility component that doesn't render anything
};

// Usage example:
// <ToastFeedback 
//   message="Command executed successfully" 
//   type="success"
//   haptic={true}
//   audio={true}
// />