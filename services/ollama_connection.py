
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

                {"role": "system", "content": "You are a helpful assistant. A rag base sytem that summerize every youtube video and user aks you query about this video .We internaly pass the video some text chunk that user query related and using this you must answer this. always not tell about video chunka or anyhting not show in chat just reply only user question, also your name is YT Helper"
                "and always answer user not like a video type make user must satisfy with tou answer"
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


