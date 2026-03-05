from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY=os.getenv('GROK_API_KEY')

llm = ChatGroq(
    model='llama-3.1-8b-instant',
    api_key=GROK_API_KEY,
    temperature=0
)


result = llm.invoke([
    {"role": "user", "content": "Testing. Just say hi and hello world and nothing else."}
])

print(result)