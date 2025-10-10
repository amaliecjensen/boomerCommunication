#husk at give persist_directory for at min chromadb ikke skal køre in-memory mode
#formål
#Når en ny mail kommer kan jeg se: har jeg fået mails fra samme afsender før? var de tidligere mails markeret som vigtige?
import chromadb

def setup_database():
    client = chromadb.PersistentClient("./chroma_db") #opretter database i mappen
    collection = client.get_or_create_collection(
        name="email_collection"
    )
    return client, collection

client, collection = setup_database()



def save_emails(sender, subject, body, isImportant, historyid):
    unique_id = f"{sender}_{historyid}"  # Kombinerer sender og historyid

    document_text = f"{subject}\n{body}" #bruges som tekst der kan søges på


#simple typer som chroma kan filtrere på
    metadata = {
  "sender": sender,
  "subject": subject,
  "isImportant": isImportant,
  "historyid": historyid
     }

    collection.add(
        ids=[unique_id],
        documents=[document_text],
        metadatas=[metadata]
    )
    print(f"saved data to DB")
    