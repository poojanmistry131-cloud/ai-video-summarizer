# 🎬 AI Video Summarizer

Paste a YouTube video or direct MP4 link and get its transcript, AI-generated summary, quiz, and downloadable PDF report.

## How to Run (For Beginners)

### Before you start

Install **Python 3.10 or higher** on your computer:

1. Go to https://www.python.org/downloads/ and download Python.
2. Run the installer and tick **"Add Python to PATH"**.
3. Click **Install Now**.
4. Install **VS Code** from https://code.visualstudio.com/ if you do not have it.
5. Install **FFmpeg** and make sure it is available on your PATH:
   https://ffmpeg.org/download.html
6. Get a free API key from https://console.groq.com/keys.

To check that Python is installed, open Command Prompt and type `python --version`.

### Steps

1. Open this repository page on GitHub.
2. Click the green **Code** button, then click **Download ZIP**.
3. Open your Downloads folder and right-click the ZIP file. Click **Extract All**.
4. Open **VS Code**.
5. Press `Ctrl + Shift + E` to open the Explorer panel.
6. Click **Open Folder** and select the extracted project folder. Choose the folder that contains `README.md`, `backend`, and `frontend`.
7. Open the VS Code terminal by pressing `` Ctrl + ` `` (the backtick key, just below Esc).
8. Create a Python environment and install the project libraries:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
   ```

9. Create a file named `.env` inside the `backend` folder. Add your Groq API key:

   ```dotenv
   GROQ_API_KEY=your_groq_api_key
   ```

   Replace `your_groq_api_key` with your key. Do not share it or upload your `.env` file.

10. Open a **second terminal** in VS Code. In the first terminal, start the backend:

    ```powershell
    .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000 --app-dir backend
    ```

11. In the second terminal, start the frontend:

    ```powershell
    .\.venv\Scripts\python.exe -m streamlit run frontend\app.py
    ```

12. Open the local Streamlit address shown in the terminal (usually http://localhost:8501).
13. Paste a YouTube or direct MP4 URL and click **Analyze Video**.

Keep both terminals running while you use the app.

## Features

- Accepts YouTube links and direct MP4 links
- Transcribes speech with OpenAI Whisper
- Creates an AI summary and a five-question multiple-choice quiz using Groq
- Lets you answer the quiz and see your score
- Downloads the transcript and a summary-and-quiz PDF

## Requirements

- Python 3.10 or higher
- FFmpeg
- A Groq API key
- Python libraries listed in `backend/requirements.txt`

## How to Run (Using Git)

### 1. Clone the repository

```bash
git clone https://github.com/poojanmistry131-cloud/ai-video-summarizer.git
cd ai-video-summarizer
```

### 2. Create and activate a virtual environment

```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r backend/requirements.txt
```

Create `backend/.env` and set `GROQ_API_KEY` as shown in the beginner steps above. FFmpeg must also be installed and available on your PATH.

### 4. Start the application

Open two terminals in the repository folder.

Terminal 1 (backend):

```bash
python -m uvicorn app.main:app --reload --port 8000 --app-dir backend
```

Terminal 2 (frontend):

```bash
python -m streamlit run frontend/app.py
```

Open http://localhost:8501 in your browser. The API documentation is at http://127.0.0.1:8000/docs.

## Troubleshooting

- **`'python' is not recognized`** → Reinstall Python and select **"Add Python to PATH"**.
- **`No module named ...`** → From the repository folder, activate `.venv` and run `python -m pip install -r backend/requirements.txt`.
- **`ffmpeg is not recognized`** → Install FFmpeg, add it to your PATH, then restart VS Code.
- **Groq API key error** → Check that `backend/.env` contains `GROQ_API_KEY=...` and restart the backend.
- **The frontend cannot connect** → Make sure both terminals are running and the backend is listening on port `8000`.
- **Whisper runs out of memory or is slow** → The Whisper `small` model loads on the first video request and needs additional memory. Try a shorter video or use a machine with more available memory.
- **`requirements.txt` not found** → Open the project folder that contains `README.md`, `backend`, and `frontend`.

## Notes

- The first video can take longer because Whisper needs to download and load its model.
- FFmpeg extracts and splits the video's audio before transcription.
- Downloaded media and generated files are temporary application data; sample media is not needed to run the project.
