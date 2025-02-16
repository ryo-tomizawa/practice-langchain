import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
gemini_key = os.environ["GEMINI_KEY"]
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat(
    history=[
        {"role": "model", "parts": "You are a helpful assistant."},
    ]
)
response = chat.send_message("こんにちは！私はジョンといいます！")

print(response.text)