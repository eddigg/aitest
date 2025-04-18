import deepspeech
import logging
import numpy as np
import os
from typing import Dict, Any
from pydub import AudioSegment
import io
import time

# Setup logging if not already configured
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
if not logging.getLogger().handlers:
    logging.basicConfig(
        filename=os.path.join(log_dir, "ml_benchmarks.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

class DeepSpeechError(Exception):
    """Custom exception for DeepSpeech transcription errors"""
    def __init__(self, error_type: str, message: str):
        self.error_type = error_type
        super().__init__(f"{error_type}: {message}")

class DeepSpeechTranscriber:
    def __init__(self, model_path: str):
        """Initialize DeepSpeech model for transcription
        
        Args:
            model_path: Path to DeepSpeech model file (.pbmm)
        """
        try:
            self.model = deepspeech.Model(model_path)
            logging.info(f"Loaded DeepSpeech model from {model_path}")
        except Exception as e:
            logging.error(f"Failed to load DeepSpeech model: {str(e)}")
            raise DeepSpeechError("MODEL_LOAD_ERROR", f"Failed to load DeepSpeech model: {str(e)}")

    def preprocess_audio(self, audio_data: bytes) -> np.ndarray:
        """Convert audio data to format suitable for DeepSpeech
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Numpy array of audio samples
        """
        try:
            # Convert to WAV format
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            
            # Convert to numpy array
            samples = np.array(audio.get_array_of_samples())
            
            return samples
        except Exception as e:
            logging.error(f"Audio preprocessing failed: {str(e)}")
            raise DeepSpeechError("PREPROCESSING_ERROR", f"Failed to preprocess audio: {str(e)}")

    def transcribe(self, audio_data: bytes) -> Dict[str, Any]:
        """Transcribe audio data to text using DeepSpeech
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Dictionary containing transcription result and metadata
        """
        try:
            # Preprocess audio
            audio_samples = self.preprocess_audio(audio_data)
            
            # Transcribe
            start_time = time.time()
            text = self.model.stt(audio_samples)
            inference_time = time.time() - start_time
            
            # Log performance metrics
            logging.info(f"DeepSpeech transcription completed in {inference_time:.2f}s")
            
            return {
                "text": text,
                "inference_time": inference_time,
                "model": "deepspeech"
            }
            
        except DeepSpeechError as e:
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logging.error(f"Transcription failed: {str(e)}")
            raise DeepSpeechError("TRANSCRIPTION_ERROR", f"Failed to transcribe audio: {str(e)}")

# Example usage:
# transcriber = DeepSpeechTranscriber('path/to/model.pbmm')
# result = transcriber.transcribe(audio_bytes)
# print(result["text"])