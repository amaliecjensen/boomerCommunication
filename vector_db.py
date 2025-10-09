#husk at give persist_directory for at min chromadb ikke skal køre in-memory mode
#hej
import chromadb

def setup_database():
    client = chromadb.PersistentClient("./chroma_db") #opretter database i mappen
    collection = client.get_or_create_collection(
        name="email"
    )
    return client, collection

client, collection = setup_database()

def save_emails(sender, subject, body, isImportant, historyid):

    data = {
        ids=[],
        embeddings=[],
        metadatas=[],
        documents=[]
    }

    collection.add()
    print(f"saved data to DB")
    