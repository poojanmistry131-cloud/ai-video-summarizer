from groq import Groq
import os
import json
import re

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MAX_TRANSCRIPT_CHARS = 10000

def generate_quiz(transcript: str) -> list:
    if not transcript.strip():
        raise ValueError("Transcript is empty, cannot generate quiz.")

    truncated = transcript[:MAX_TRANSCRIPT_CHARS]

    prompt = f"""You are an expert quiz creator. Based on the following video transcript, generate exactly 5 multiple-choice questions.

Rules:
- Each question must have exactly 4 options labeled A, B, C, D
- Only one option is correct
- Return ONLY valid JSON, no extra text, no markdown code blocks

Return this exact JSON structure:
[
  {{
    "question": "Question text here?",
    "options": {{
      "A": "Option A text",
      "B": "Option B text",
      "C": "Option C text",
      "D": "Option D text"
    }},
    "answer": "A",
    "explanation": "Brief explanation of why this is correct"
  }}
]

Transcript:
{truncated}

JSON Quiz:"""

    response = client.chat.completions.create(
      model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a quiz generation expert. Always respond with valid JSON only. No markdown."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1500,
        temperature=0.4
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)
    raw = raw.strip()

    try:
        quiz = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Quiz JSON parsing failed: {e}")

    if not isinstance(quiz, list) or len(quiz) == 0:
        raise ValueError("Quiz generation returned invalid data.")

    return quiz