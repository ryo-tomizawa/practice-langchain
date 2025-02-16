import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.environ['OPEN_AI_KEY']

model = ChatOpenAI(api_key=api_key, model="gpt-4o-mini", temperature=0)
messages = [
    SystemMessage("You are a helpful assistant."),
    HumanMessage("こんにちは！私はジョンといいます！"),
]

ai_message = model.invoke(messages)
print(ai_message.content)