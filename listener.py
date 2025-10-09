from google.cloud import pubsub_v1
import json
from twilio.rest import Client
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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"] #tillader mig at læse mails
PROJECT_ID = "n8namalie"  
SUBSCRIPTION_ID = "gmail-sub"    

def get_new_emails(history_id):
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        service = build("gmail", "v1", credentials=creds)
        
        # Hent seneste emails direkte i stedet for history
        result = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            maxResults=1
        ).execute()
        
        emails = []
        messages = result.get('messages', [])
        
        for message in messages:
            msg_id = message['id']
            
            msg = service.users().messages().get(userId='me', id=msg_id, format='metadata').execute()
            headers = {h['name']: h['value'] for h in msg['payload'].get('headers', [])}
            
            emails.append({
                'sender': headers.get('From', 'Unknown'),
                'subject': headers.get('Subject', 'No Subject'),
                'body': f"Email fra {headers.get('From', 'Unknown')}"  
            })
        
        return emails
    except Exception as e:
        return []

def evaluate_email(sender, subject, body):
    prompt = f"""
You are an email assistant. You receive an email with the following information:

Sender: {sender}
Subject: {subject}
Content: {body}

1. Evaluate if the email is important for the recipient, based on criteria:
   - Whether it requires action, decision or response.
   - Whether it comes from a known sender (manager, customer, business partner).
   - Whether it contains time-critical information (deadline, meeting, approval).
   - Whether it relates to a current project or responsibility.

Answer precisely with valid JSON max using 20 words(no trailing commas):
{{
  "isImportant": true,
  "summary": [very short summary max 10 words]"
}}
"""
    try:
        response = llm.invoke(prompt)
        response_text = response.content.strip()
        
        import re #regrex
        response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)
                
        return json.loads(response_text) #denne linje udtrækker svaret uden whitespaces
    except Exception as e:
        print(f"Failed evaluation: {e}")
        return {"isImportant": False, "reason": "Fejl ved evaluering", "summary": ""}
    
def send_message_to_phone(message_data):
    account_sid = os.environ["account_sid"]
    auth_token = os.environ["auth_token"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+12182745166',
        body=message_data,
        to='+4520209628'
    )

def handle_gmail_notifications(message):
    try:
        try:
            data = json.loads(base64.b64decode(message.data).decode("utf-8"))
        except:
            data = json.loads(message.data.decode("utf-8"))
        
        print("New gmail notification!!:")
        
        # Tjek historyId og hent emails
        if 'historyId' not in data:
            message.ack()
            return
            
        new_emails = get_new_emails(data['historyId'])

        if new_emails:
            
            # Evaluer hver email
            for email in new_emails:
                evaluation = evaluate_email(email['sender'], email['subject'], email['body'])
                
                if evaluation['isImportant']:
                   send_message_to_phone(f"You have received an important email! {evaluation['summary']}")
                   print(f"MESSAGE SENT TO PHONE")
                else:
                    print("Normal email")
        else:
            print("No new emails found")

        message.ack() #sender besked til google cloud pub/sub om at beskeden blev behandlet succesfuldt

    except Exception as e:
        message.nack()

def main():
    subscriber = pubsub_v1.SubscriberClient() #opretter forbindelse til google cloud pub/sub
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=handle_gmail_notifications) #kalder handle_gmail_notifications hver gange en besked kommer

    try:
        streaming_pull_future.result()  # blokerer og holder connection åben
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    main()

