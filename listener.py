from google.cloud import pubsub_v1
import json
import base64

PROJECT_ID = "YOUR_PROJECT_ID"   # fx "my-gmail-project"
SUBSCRIPTION_ID = "gmail-sub"    # du skal have oprettet en subscription i Pub/Sub

def callback(message):
    try:
        # Decode Pub/Sub message
        data = json.loads(base64.b64decode(message.data).decode("utf-8"))
        print("📩 Ny Gmail notifikation:")
        print(json.dumps(data, indent=2))

        # Det vigtigste felt er historyId
        # {
        #   "emailAddress": "din_email@gmail.com",
        #   "historyId": "1234567"
        # }

        message.ack()

    except Exception as e:
        print("Fejl i callback:", e)
        message.nack() #tells google c that the message not got treated

def main():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    print(f"Lytter på Pub/Sub subscription: {subscription_path}")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result()  # blokerer og holder connection åben
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    main()
