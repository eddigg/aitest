import whisper
import logging
from pydub import AudioSegment
import io
import os
from typing import Optional, Dict, Any

# Setup logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "ml_benchmarks.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class AudioTranscriptionError(Exception):
    """Custom exception for audio transcription errors"""
    def __init__(self, error_type: str, message: str):
        self.error_type = error_type
        super().__init__(f"{error_type}: {message}")

class WhisperTranscriber:
    def __init__(self, model_name: str = "tiny.en"):
        """Initialize Whisper model for transcription
        
        Args:
            model_name: Name of the Whisper model to use (tiny.en is fastest)
        """
        try:
            self.model = whisper.load_model(model_name)
            logging.info(f"Loaded Whisper model: {model_name}")
        except Exception as e:
            logging.error(f"Failed to load Whisper model: {str(e)}")
            raise AudioTranscriptionError("MODEL_LOAD_ERROR", f"Failed to load Whisper model: {str(e)}")

    def preprocess_audio(self, audio_data: bytes) -> str:
        """Convert audio data to WAV format suitable for Whisper
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Path to temporary WAV file
        """
        try:
            # Convert to WAV format
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            audio = audio.set_frame_rate(16000).set_channels(1)  # Whisper expects 16kHz mono
            
            # Save to temporary file
            temp_path = os.path.join(os.path.dirname(__file__), "temp.wav")
            audio.export(temp_path, format="wav")
            return temp_path
        except Exception as e:
            logging.error(f"Audio preprocessing failed: {str(e)}")
            raise AudioTranscriptionError("PREPROCESSING_ERROR", f"Failed to preprocess audio: {str(e)}")

    def transcribe(self, audio_data: bytes) -> Dict[str, Any]:
        """Transcribe audio data to text
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Dictionary containing transcription result and metadata
        """
        try:
            # Preprocess audio
            temp_path = self.preprocess_audio(audio_data)
            
            # Transcribe
            start_time = time.time()
            result = self.model.transcribe(temp_path)
            inference_time = time.time() - start_time
            
            # Log performance metrics
            logging.info(f"Transcription completed in {inference_time:.2f}s")
            
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return {
                "text": result["text"],
                "inference_time": inference_time,
                "language": result.get("language", "en"),
                "segments": result.get("segments", [])
            }
            
        except AudioTranscriptionError as e:
            # Re-raise custom exceptions
            raise
        except Exception as e:
            logging.error(f"Transcription failed: {str(e)}")
            raise AudioTranscriptionError("TRANSCRIPTION_ERROR", f"Failed to transcribe audio: {str(e)}")

# Example usage:
# transcriber = WhisperTranscriber()
# result = transcriber.transcribe(audio_bytes)
# print(result["text"])