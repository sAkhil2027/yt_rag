import os
from groq import Groq
from config import GROQ_API_KEY

def get_groq_api_keys() -> list[str]:
    raw = GROQ_API_KEY or os.getenv("GROQ_API_KEY") or ""
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    if not keys:
        raise ValueError("GROQ_API_KEY is not set in environment variables or .env file.")
    return keys

def groq_model_stream(prompt: str, chunk_list: list):
    api_keys = get_groq_api_keys()
    client = Groq(api_key=api_keys[0])
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are YT Helper, a helpful assistant."},
            {"role": "user", "content": f"User question: {prompt}\n\nVideo context: {chunk_list}"}
        ],
        stream=True
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta

def groq_model(prompt: str, chunk_list: list) -> str:
    return "".join(groq_model_stream(prompt, chunk_list))
