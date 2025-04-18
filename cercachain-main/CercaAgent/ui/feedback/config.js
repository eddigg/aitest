// Feedback system configuration
export const feedbackConfig = {
  // Visual feedback settings
  visual: {
    enabled: true,
    toast: {
      position: 'bottom-right',
      autoClose: 3000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true
    },
    lottie: {
      defaultWidth: 100,
      defaultHeight: 100,
      defaultLoop: true,
      defaultAutoplay: true
    }
  },

  // Audio feedback settings
  audio: {
    enabled: true,
    tts: {
      endpoint: '/api/tts',
      fallbackEndpoint: '/api/tts_polly',
      defaultVoice: 'en-US',
      defaultRate: 1,
      defaultPitch: 1
    },
    sounds: {
      success: '/assets/sounds/success.mp3',
      error: '/assets/sounds/error.mp3',
      warning: '/assets/sounds/warning.mp3',
      notification: '/assets/sounds/notification.mp3'
    }
  },

  // Haptic feedback settings
  haptic: {
    enabled: true,
    patterns: {
      success: [100],
      error: [100, 100, 100],
      warning: [200, 100, 200],
      notification: [50],
      processing: [50, 100, 50]
    }
  },

  // Analytics settings
  analytics: {
    enabled: true,
    providers: {
      mixpanel: true,
      ga4: true,
      hotjar: true
    },
    events: {
      trackFeedback: true,
      trackInteractions: true,
      trackErrors: true
    }
  }
};