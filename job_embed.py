
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from pymongo import MongoClient
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

openapi_key = os.getenv('OPENAI_API_KEY')
pinecone_key = os.getenv('PINECONE_API_KEY')
environment = os.getenv('PINECONE_ENVIRONMENT')

# Set environment variables
os.environ["OPENAI_API_KEY"] = openapi_key

# Initialize Pinecone
pc = PineconeClient(
    api_key=pinecone_key
)
# Check if the index exists and create it if not
if 'crewdogjobs' not in pc.list_indexes().names():
    pc.create_index(
        name='crewdogjobs',
        dimension=1536,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='gcp',
            region='starter'
        )
    )

index = pc.Index('crewdogjobs')
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

client = MongoClient("mongodb+srv://shahbazkhan6732:AXkoh5XMDQBo3FyW@linkdin.q0omyf7.mongodb.net/?retryWrites=true&w=majority&appName=linkdin")

db = client['job_scraper']
linkedin_job = db["jobs"]

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

