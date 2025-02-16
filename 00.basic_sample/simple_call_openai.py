import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_key = os.environ['OPEN_AI_KEY']
client = OpenAI(api_key=openai_key)

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "こんにちは！私はジョンといいます！"},
    ],
)
print(response.to_json(indent=2))