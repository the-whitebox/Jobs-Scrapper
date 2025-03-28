
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from pymongo import MongoClient
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

openapi_key = os.getenv('OPENAI_API_KEY')
pinecone_key = os.getenv('PINECONE_API_KEY')
mongo_uri = os.getenv('MONGO_URI')
# Set environment variables
os.environ["OPENAI_API_KEY"] = openapi_key


username = "crewdog"
password = "crewdog@1234"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)
client = f"mongodb+srv://{encoded_username}:{encoded_password}@crewdogjobs.9fhrv.mongodb.net/?retryWrites=true&w=majority&appName=crewdogjobs"
 
client = MongoClient(client)
db = client['jobs']

linkedin_job = db['reedco_jobs']

# Initialize Pinecone
pc = PineconeClient(
    api_key=pinecone_key
)

index = pc.Index('readco-jobs')
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def linkedin_automate(record):
    print("----------------- in linkdin automate method----------------", record)

    document = {
        "metadata": {
            "job_title": record.get('position'),
            "job_source": record.get('job_source'),
            "job_id": record.get('job_id'),
            "job_status": record.get('job_status'),
            "location": record.get("location"),
            "hiring_person": record.get("hiring_person"),
            "text": str(record)
        }
    }
    keys_to_delete = [
        "hiring_person_linkedin_link",
        "other_information",
        "job_id",
        "search_keywords",
        "time_stamp",
        "job_status",
        "_id",
    ]

    for i in keys_to_delete:
        if 'search_keywords' in record:
            if 'location' in record['search_keywords']:
                del record['search_keywords']['location']
                del record[i]

    page_content = str(record)
    metadata = document.get("metadata")
    doc = Document(page_content=page_content, metadata=metadata)
    doc_dict = {
        'vector': embeddings.embed_query(doc.page_content),
        'metadata': doc.metadata
    }

    if index.upsert(
            vectors=[{
                'id': doc_dict.get("metadata").get("job_id"),
                'values': doc_dict.get("vector"),
                'metadata': doc_dict.get("metadata")
            }]
    ):
        return True

    print("-----------------Exited from linkdin automate method----------------")
