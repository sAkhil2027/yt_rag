
import os
from dotenv import load_dotenv

from langfuse.openai import OpenAI

load_dotenv()

# Configure the OpenAI client to use http://localhost:11434/v1 as base url
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

def llama3_model(prompt:str, chunk_list:list):

    try:
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


