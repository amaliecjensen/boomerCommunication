from google.cloud import pubsub_v1
import json
import base64
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

load_dotenv() #load env variables
open_api_key = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(api_key=open_api_key, model="gpt-3.5-turbo", temperature=0)

# Sæt Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"] #tillader mig at læse mails
PROJECT_ID = "n8namalie"  
SUBSCRIPTION_ID = "gmail-sub"    

def get_new_emails(history_id):
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        service = build("gmail", "v1", credentials=creds)
        
        result = service.users().history().list(
            userId='me',
            startHistoryId=history_id
        ).execute()
        
        # Parse emails fra history
        emails = []
        for history_item in result.get('history', []):
            for message in history_item.get('messagesAdded', []):
                msg_id = message['message']['id']
                
                msg = service.users().messages().get(userId='me', id=msg_id).execute()
                
                headers = msg['payload'].get('headers', [])
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                
                body = ""
                if 'parts' in msg['payload']:
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/plain' and part['body'].get('data'):
                            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
                elif msg['payload']['body'].get('data'):
                    body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
                
                emails.append({
                    'sender': sender,
                    'subject': subject,
                    'body': body[:300]
                })
        
        return emails
    except Exception as e:
        print(f"Fejl ved hentning af emails: {e}")
        return []

def evaluate_email(sender, subject, body):
    prompt = f"""
You are an email assistant. You receive an email with the following information:

Sender: {sender}
Subject: {subject}
Content: {body}

1. Evaluate if the email is important for the recipient, based on criteria such as:
   - Whether it requires action, decision or response.
   - Whether it comes from a known sender (manager, customer, business partner).
   - Whether it contains time-critical information (deadline, meeting, approval).
   - Whether it relates to a current project or responsibility.

Answer precisely with:
{{
  "isImportant": true/false,
  "reason": "brief explanation",
  "summary": "brief summary (max 3 sentences, only if isImportant=true)"
}}
"""
    try:
        response = llm.invoke(prompt)
        return json.loads(response.content.strip())
    except Exception as e:
        print(f"Fejl ved evaluering: {e}")
        return {"isImportant": False, "reason": "Fejl ved evaluering", "summary": ""}

def handle_gmail_notifications(message):
    try:
        data = json.loads(base64.b64decode(message.data).decode("utf-8")) #decoder da vi modtager data krypteret
        print("New gmail notification:")
        print(json.dumps(data, indent=2))
        history_id = data['historyId']

        # metodekals
        new_emails = get_new_emails(history_id)

        if new_emails:
            print(f"Found {len(new_emails)} new emails")
            
            # Evaluer hver email
            for email in new_emails:
                # Kald evaluate_email for at lave evt. resume
                evaluation = evaluate_email(
                    email['sender'], 
                    email['subject'], 
                    email['body']
                )
                
                if evaluation['isImportant']:
                    print("IMPORTANT EMAIL found!")
                    print(f"Grund: {evaluation['reason']}")
                    print(f"Resume: {evaluation['summary']}")
                else:
                    print("Normal email")
                    print(f"Grund: {evaluation['reason']}")
        else:
            print("No new emails found")

        message.ack() #sender besked til google cloud pub/sub om at beskeden blev behandlet succesfuldt

    except Exception as e:
        print("Error in gmail notification handler:", e)
        message.nack()

def main():
    subscriber = pubsub_v1.SubscriberClient() #opretter forbindelse til google cloud pub/sub
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    print(f"Lytter på Pub/Sub subscription: {subscription_path}")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=handle_gmail_notifications) #kalder handle_gmail_notifications hver gange en besked kommer

    try:
        streaming_pull_future.result()  # blokerer og holder connection åben
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    main()