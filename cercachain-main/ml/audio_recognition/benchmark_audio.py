import logging
import time
import os
from typing import Dict, Any, List
from whisper_inference import WhisperTranscriber, AudioTranscriptionError
from deepspeech_inference import DeepSpeechTranscriber, DeepSpeechError

# Setup logging if not already configured
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
if not logging.getLogger().handlers:
    logging.basicConfig(
        filename=os.path.join(log_dir, "ml_benchmarks.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

class AudioBenchmark:
    def __init__(self):
        """Initialize transcription models for benchmarking"""
        self.whisper = WhisperTranscriber(model_name="tiny.en")
        # DeepSpeech model path should be configured based on installation
        self.deepspeech = None  # Initialize when model path is available
        
    def benchmark_whisper(self, audio_data: bytes) -> Dict[str, Any]:
        """Benchmark Whisper transcription
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Dictionary containing transcription result and performance metrics
        """
        try:
            start_time = time.time()
            result = self.whisper.transcribe(audio_data)
            total_time = time.time() - start_time
            
            metrics = {
                "model": "whisper",
                "total_time": total_time,
                "inference_time": result["inference_time"],
                "preprocessing_time": total_time - result["inference_time"],
                "success": True,
                "text": result["text"]
            }
            
            logging.info(f"Whisper Benchmark: {metrics}")
            return metrics
            
        except AudioTranscriptionError as e:
            logging.error(f"Whisper benchmark failed: {str(e)}")
            return {
                "model": "whisper",
                "success": False,
                "error": str(e)
            }
    
    def benchmark_deepspeech(self, audio_data: bytes, model_path: str) -> Dict[str, Any]:
        """Benchmark DeepSpeech transcription
        
        Args:
            audio_data: Raw audio bytes
            model_path: Path to DeepSpeech model file
            
        Returns:
            Dictionary containing transcription result and performance metrics
        """
        try:
            if self.deepspeech is None:
                self.deepspeech = DeepSpeechTranscriber(model_path)
                
            start_time = time.time()
            result = self.deepspeech.transcribe(audio_data)
            total_time = time.time() - start_time
            
            metrics = {
                "model": "deepspeech",
                "total_time": total_time,
                "inference_time": result["inference_time"],
                "preprocessing_time": total_time - result["inference_time"],
                "success": True,
                "text": result["text"]
            }
            
            logging.info(f"DeepSpeech Benchmark: {metrics}")
            return metrics
            
        except DeepSpeechError as e:
            logging.error(f"DeepSpeech benchmark failed: {str(e)}")
            return {
                "model": "deepspeech",
                "success": False,
                "error": str(e)
            }
    
    def run_benchmarks(self, audio_data: bytes, deepspeech_model_path: str = None) -> List[Dict[str, Any]]:
        """Run benchmarks for all available transcription models
        
        Args:
            audio_data: Raw audio bytes
            deepspeech_model_path: Optional path to DeepSpeech model file
            
        Returns:
            List of benchmark results for each model
        """
        results = [self.benchmark_whisper(audio_data)]
        
        if deepspeech_model_path:
            results.append(self.benchmark_deepspeech(audio_data, deepspeech_model_path))
        
        return results

# Example usage:
# benchmark = AudioBenchmark()
# results = benchmark.run_benchmarks(audio_bytes, 'path/to/deepspeech.pbmm')
# for result in results:
#     if result["success"]:
#         print(f"{result['model']}: {result['total_time']:.2f}s - {result['text']}")
#     else:
#         print(f"{result['model']} failed: {result['error']}")