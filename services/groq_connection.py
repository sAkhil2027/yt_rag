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
    candidate_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"]
    for api_key in api_keys:
        client = Groq(api_key=api_key)
        for model_name in candidate_models:
            try:
                stream = client.chat.completions.create(
                    model=model_name,
        messages=[
            {"role": "system", "content": "You are YT Helper, a helpful assistant."},
            {"role": "user", "content": f"User question: {prompt}\n\nVideo context: {chunk_list}"}
        ],
        stream=True
    )
                    stream=True
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta
                return
            except Exception:
                continue

def groq_model(prompt: str, chunk_list: list) -> str:
    return "".join(groq_model_stream(prompt, chunk_list))
