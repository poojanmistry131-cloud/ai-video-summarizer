# AI Video Summarizer

Turn a YouTube video or a direct MP4 URL into a transcript, an AI-generated summary, a five-question quiz, and a downloadable PDF report.

## Features

- Downloads YouTube videos and direct MP4 links.
- Transcribes audio locally with OpenAI Whisper.
- Generates a summary and multiple-choice quiz using the Groq API.
- Provides a Streamlit interface and a FastAPI backend.
- Offers transcript and PDF downloads.

## Requirements

- Python 3.10 or newer
- [FFmpeg](https://ffmpeg.org/download.html) installed and available on your `PATH`
- A [Groq API key](https://console.groq.com/keys)
- Enough memory to run the Whisper `small` model. It is loaded on the first transcription request.

## Setup on Windows

Run these commands from the repository root in PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Create `backend\.env` and add your Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Do not commit your `.env` file or share your API key.

## Run the application

Open two terminals at the repository root.

In the first terminal, start the API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000 --app-dir backend
```

In the second terminal, start the Streamlit interface:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend\app.py
```

Open the Streamlit URL printed in the terminal (usually <http://localhost:8501>). The API is available at <http://127.0.0.1:8000>, with interactive documentation at <http://127.0.0.1:8000/docs>.

## Notes

- The first transcription downloads and loads the Whisper model, so it may take longer and need additional memory.
- FFmpeg is used to extract and split audio.
- Temporary video/audio files and generated transcript, summary, and PDF files are written under `data` while the application runs. Sample data is not required in the repository.
