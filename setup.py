import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # loader enviroment variables

# Get openai key
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Initialize ChatGPT, model 3.5--turbo(hurtig og effektiv, temp=o (konsistente og forudsigelige svar))
chat = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def setup_watch():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    request = {
        "labelIds": ["INBOX"],  # overvåg indbakken
        "topicName": "projects/YOUR_PROJECT_ID/topics/gmail-notifications"
    }

    response = service.users().watch(userId="me", body=request).execute()
    print("Min watch er sat op:", response)

if __name__ == "__main__":
    setup_watch()
