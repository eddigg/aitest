from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from voice_recognition.transcribe import transcribe_audio
from voice_recognition.classify import classify_intent
from command_mapping.action_map import get_action
from event_handling.execute import execute_action

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

@app.post("/process_audio")
async def process_audio(audio: UploadFile = File(...)):
    audio_data = await audio.read()
    transcription = transcribe_audio(audio_data)
    intent = classify_intent(transcription)
    action = get_action(intent)
    result = execute_action(intent, action)
    return {"transcription": transcription, "intent": intent, **result}

# Stub for future video processing
@app.post("/process_video")
async def process_video():
    return {"status": "not_implemented", "message": "Video processing not available in MVP"}

# Stub for future text processing
@app.post("/process_text")
async def process_text():
    return {"status": "not_implemented", "message": "Text processing not available in MVP"}