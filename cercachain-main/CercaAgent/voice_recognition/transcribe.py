from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
import io

processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

def transcribe_audio(audio_data: bytes) -> str:
    # Convert audio to WAV if needed
    audio = AudioSegment.from_file(io.BytesIO(audio_data))
    audio = audio.set_frame_rate(16000).set_channels(1)  # Whisper expects 16kHz mono
    audio.export("temp.wav", format="wav")

    # Process audio
    input_features = processor(audio.get_array_of_samples(), sampling_rate=16000, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription