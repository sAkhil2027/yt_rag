import os
from groq import Groq
from config import GROQ_API_KEY


def get_groq_api_keys() -> list[str]:
    """Parses single or comma-separated Groq API keys from environment."""
    raw = GROQ_API_KEY or os.getenv("GROQ_API_KEY") or ""
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    if not keys:
        raise ValueError("GROQ_API_KEY is not set in environment variables or .env file.")
    return keys


def groq_model_stream(prompt: str, chunk_list: list):
    """
    Stream tokens from Groq API with multi-model quota failover,
    multi-key rotation, and dynamic context trimming on 429 rate limits.
    """
    api_keys = get_groq_api_keys()
    
    # Active verified models across distinct rate limit buckets on Groq Cloud
    candidate_models = [
        "llama-3.3-70b-versatile",  # Highest quality reasoning
        "llama-3.1-8b-instant",     # 10x higher TPM limit (14,400 TPM)
        "mixtral-8x7b-32768",       # Separate MoE bucket
        "gemma2-9b-it"              # Google architecture on Groq
    ]

    # Context attempts: full context first, then trimmed context if 429 hit
    context_attempts = [chunk_list]
    if isinstance(chunk_list, list) and len(chunk_list) > 1:
        context_attempts.append(chunk_list[: len(chunk_list) // 2])
    elif isinstance(chunk_list, str) and len(chunk_list) > 1000:
        context_attempts.append(chunk_list[: len(chunk_list) // 2])

    last_exception = None

    for api_key in api_keys:
        client = Groq(api_key=api_key)
        for model_name in candidate_models:
            for context_data in context_attempts:
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
                                "content": f"User question: {prompt}\n\nVideo context: {context_data}"
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
                    err_msg = str(e).lower()
                    if "429" in err_msg or "rate limit" in err_msg:
                        print(f"[WARN] Groq 429 Rate Limit on model {model_name}. Attempting next quota/bucket...")
                        continue
                    # Non-429 error on this model (e.g. model outage) -> move to next model
                    break

    raise Exception(f"Groq API Error across all models and keys: {last_exception}")


def groq_model(prompt: str, chunk_list: list) -> str:
    """Non-streaming wrapper for MCP server and standard queries."""
    return "".join(groq_model_stream(prompt, chunk_list))
