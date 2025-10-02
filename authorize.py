from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import sys

# Vi skal kun bruge readonly adgang i starten
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    # Check for credentials file
    credentials_file = "credentials.json"
    
    if not os.path.exists(credentials_file):
        print(f"❌ Fejl: {credentials_file} findes ikke!")
        print("\n📋 For at få Google OAuth credentials:")
        print("1. Gå til https://console.cloud.google.com/")
        print("2. Opret et nyt projekt eller vælg eksisterende")
        print("3. Aktiver Gmail API")
        print("4. Gå til 'Credentials' > 'Create Credentials' > 'OAuth client ID'")
        print("5. Vælg 'Desktop application'")
        print("6. Download JSON filen og gem den som 'credentials.json' i dette projekt")
        print("\n💡 Tip: Filen skal hedde 'credentials.json' og ligge i samme mappe som dette script")
        sys.exit(1)
    
    try:
        # indlæs client_secret JSON fra Google
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)

        # gem token.json til senere brug
        with open("token.json", "w") as token:
            token.write(creds.to_json())

        print("✅ Login OK – token gemt!")
        
    except Exception as e:
        print(f"❌ Fejl under godkendelse: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
