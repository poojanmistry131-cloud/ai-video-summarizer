from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.video_service import download_video
from app.services.audio_service import extract_audio
from app.services.chunk_service import chunk_audio
from app.services.stt_service import transcribe_chunks
from app.services.summary_service import summarize_text
from app.services.quiz_service import generate_quiz
from app.services.pdf_service import create_pdf
import os

app = FastAPI(title="AI Video Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

class SummaryResponse(BaseModel):
    transcript: str
    summary: str
    quiz: list
    pdf_path: str

@app.get("/")
def root():
    return {"message": "AI Video Summarizer API is running"}

@app.post("/process", response_model=SummaryResponse)
def process_video(request: VideoRequest):
    url = request.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    try:
        video_path = download_video(url)
        audio_path = extract_audio(video_path)
        chunk_paths = chunk_audio(audio_path)
        transcript = transcribe_chunks(chunk_paths)

        import pathlib
        DATA_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "data" / "text"
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(DATA_DIR / "transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript)

        summary = summarize_text(transcript)
        with open(DATA_DIR / "summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)

        quiz = generate_quiz(transcript)
        pdf_path = create_pdf(summary, quiz)

        return SummaryResponse(
            transcript=transcript,
            summary=summary,
            quiz=quiz,
            pdf_path=pdf_path
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))