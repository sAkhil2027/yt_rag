import os
from groq import Groq
from config import GROQ_API_KEY


def groq_model_stream(prompt: str, chunk_list: list):
    """
    Stream tokens from Groq API using available active chat models.
    """
    api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables or .env file.")

    client = Groq(api_key=api_key)

    # List of active chat models on Groq in priority order
    candidate_models = [
        "groq/compound",
        "groq/compound-mini",
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3.6-27b"
    ]

    last_exception = None
    for model_name in candidate_models:
        try:
            stream = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are YT Helper, a helpful assistant. You summarize YouTube video content and answer user queries based on video transcript context. "
                            "Always respond naturally and directly to the user's question without mentioning transcript chunks, video context, or internal data structures. "
                            "Your response must always be written in paragraph form only. Never format answers using tables, charts, or graphs."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"User question: {prompt}\n\nVideo context: {chunk_list}"
                    }
                ],
                stream=True
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
            return
        except Exception as e:
            last_exception = e
            continue

    raise Exception(f"Groq API Error: {last_exception}")


def groq_model(prompt: str, chunk_list: list) -> str:
    """
    Non-streaming wrapper for MCP server and standard REST queries.
    Reuses groq_model_stream to eliminate code duplication.
    """
    return "".join(groq_model_stream(prompt, chunk_list))
