
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in .env")

client = Groq(api_key=GROQ_API_KEY)

def ask_llm(messages):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.2,
            max_tokens=700
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM Error: {str(e)}"
