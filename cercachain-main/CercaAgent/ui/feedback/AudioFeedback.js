import { useFeedback } from './FeedbackManager';

class AudioFeedback {
  constructor() {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.sounds = new Map();
  }

  async loadSound(name, url) {
    try {
      const response = await fetch(url);
      const arrayBuffer = await response.arrayBuffer();
      const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
      this.sounds.set(name, audioBuffer);
    } catch (error) {
      console.error(`Failed to load sound ${name}:`, error);
    }
  }

  async playSound(name) {
    try {
      const buffer = this.sounds.get(name);
      if (!buffer) {
        throw new Error(`Sound ${name} not found`);
      }

      const source = this.audioContext.createBufferSource();
      source.buffer = buffer;
      source.connect(this.audioContext.destination);
      source.start(0);
    } catch (error) {
      console.error(`Failed to play sound ${name}:`, error);
    }
  }

  async speak(text, options = {}) {
    try {
      const response = await fetch('/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, ...options }),
      });

      if (!response.ok) {
        throw new Error('TTS request failed');
      }

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      
      return new Promise((resolve, reject) => {
        audio.onended = () => {
          URL.revokeObjectURL(audioUrl);
          resolve();
        };
        audio.onerror = reject;
        audio.play().catch(reject);
      });
    } catch (error) {
      console.error('TTS failed:', error);
      throw error;
    }
  }
}

// Hook for using AudioFeedback within React components
export const useAudioFeedback = () => {
  const { settings } = useFeedback();
  const audioFeedback = React.useMemo(() => new AudioFeedback(), []);

  const playFeedback = React.useCallback(async (name) => {
    if (settings.audio) {
      await audioFeedback.playSound(name);
    }
  }, [settings.audio, audioFeedback]);

  const speakText = React.useCallback(async (text, options) => {
    if (settings.audio) {
      await audioFeedback.speak(text, options);
    }
  }, [settings.audio, audioFeedback]);

  return { playFeedback, speakText };
};