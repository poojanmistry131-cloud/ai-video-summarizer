from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MAX_TRANSCRIPT_CHARS = 12000

def summarize_text(transcript: str) -> str:
    if not transcript.strip():
        raise ValueError("Transcript is empty, cannot summarize.")

    truncated = transcript[:MAX_TRANSCRIPT_CHARS]
    if len(transcript) > MAX_TRANSCRIPT_CHARS:
        truncated += "\n\n[Note: Transcript was truncated.]"

    prompt = f"""You are an expert content summarizer. Given the following video transcript, provide a comprehensive and well-structured summary.

Your summary should:
- Start with a brief overview (2-3 sentences)
- Cover all major topics and key points discussed
- Highlight important facts, statistics, or examples mentioned
- Be organized with clear sections using markdown headers
- Be between 300-600 words

Transcript:
{truncated}

Summary:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional content analyst. You create clear, informative summaries."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1000,
        temperature=0.5
    )

    return response.choices[0].message.content.strip()