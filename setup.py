import os
from dotenv import load_dotenv

load_dotenv() #loader enviroment variables

# Get openai key
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Initialize ChatGPT
chat = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)