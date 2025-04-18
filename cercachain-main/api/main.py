from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import logging
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
from io import BytesIO
import wave
from config import settings
import uvicorn

app = FastAPI(debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

class ErrorLog(BaseModel):
    timestamp: str
    message: str
    stack: str | None = None
    context: dict = {}

@app.post("/log-error")
async def log_error(error: ErrorLog):
    logging.error(f"Client Error: {error.message}", extra={
        "timestamp": error.timestamp,
        "stack": error.stack,
        "context": error.context
    })
    return {"status": "logged"}

@app.get("/")
async def read_root():
    return {"status": "ok"}

@app.post("/process-message")
async def process_message(message: str):
    return {
        "status": "success",
        "response": f"Processed: {message}",
        "intent": "conversation"
    }

@app.post("/process-audio")
async def process_audio(audio: UploadFile = File(...)):
    try:
        # Read the uploaded audio file
        contents = await audio.read()
        audio_bytes = BytesIO(contents)

        # Convert to wav format for speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_bytes) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            
        return {"transcription": text}
    except Exception as e:
        return {"error": str(e)}