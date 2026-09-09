
import os
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    try:
        from langfuse.openai import OpenAI
    except ImportError:
        OpenAI = None

load_dotenv()

_client = None

def get_ollama_client():
    global _client
    if _client is None:
        if OpenAI is None:
            raise RuntimeError("Neither 'openai' nor 'langfuse.openai' package is installed.")
        _client = OpenAI(
            base_url='http://localhost:11434/v1',
            api_key='ollama',
        )
    return _client


def llama3_model(prompt:str, chunk_list:list):

    try:
        client = get_ollama_client()
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are YT Helper, a helpful assistant. You summarize YouTube video content and answer user queries based on video transcript context. "
                        "Always respond naturally and directly to the user's question without mentioning transcript chunks, video context, or internal data structures. "
                        "Your response must always be written in paragraph form only. Never format answers using tables, charts, or graphs."
                    )
                },

                {"role": "user", "content": f"""
                    user: {prompt}
                    video_chunk: {chunk_list}

                """}

        ]
      
        )
        print(chunk_list)
        msg = response.choices[0].message.content
        return msg

    except Exception as e:
        raise Exception(f"error:{e}")


