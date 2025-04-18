import os
import random

def generate_garbage_audio(path='junk.wav'):
    with open(path, 'wb') as f:
        f.write(os.urandom(2048))  # 2KB of noise

def test_transcriber(transcribe_func):
    generate_garbage_audio()
    try:
        result = transcribe_func('junk.wav')
        print("Transcription result:", result)
    except Exception as e:
        print("Handled fuzz exception:", e)