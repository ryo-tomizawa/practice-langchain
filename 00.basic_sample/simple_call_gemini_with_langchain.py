import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
api_key = os.environ['GEMINI_KEY']

model = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-flash", temperature=0)
messages = [
    SystemMessage("You are a helpful assistant."),
    HumanMessage("こんにちは！私はジョンといいます！")
]

ai_message = model.invoke(messages)
print(ai_message.content)