import whisper
import os

MODEL_SIZE = "small" 

print(f"Loading Whisper model: {MODEL_SIZE} ...")
_model = whisper.load_model(MODEL_SIZE)
print("Whisper model loaded!")

def transcribe_chunks(chunk_paths: list) -> str:
    if not chunk_paths:
        raise ValueError("No audio chunks provided.")

    full_transcript = []

    for i, chunk_path in enumerate(chunk_paths):
        if not os.path.exists(chunk_path):
            raise FileNotFoundError(f"Chunk not found: {chunk_path}")

        print(f"Transcribing chunk {i+1}/{len(chunk_paths)}...")

        result = _model.transcribe(
        chunk_path,
        fp16=False,
        language=None,
        verbose=False
)

        text = result.get("text", "").strip()
        if text:
            full_transcript.append(text)

    combined = " ".join(full_transcript)

    if not combined.strip():
        raise ValueError("Transcription produced empty text.")

    return combined