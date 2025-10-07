import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
#denne py fil opretter en watch

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def setup_watch():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    request = {
        "labelIds": ["INBOX"],
        "topicName": "projects/n8namalie/topics/gmail-notifications"
    }

    response = service.users().watch(userId="me", body=request).execute()
    print("Min watch er sat op:", response)

if __name__ == "__main__":
    setup_watch()