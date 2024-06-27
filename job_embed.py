# import pymongo
# import json, os
# from langchain_openai import OpenAIEmbeddings
# import pinecone
# from langchain.docstore.document import Document
# from langchain.vectorstores import Pinecone
# from pymongo import MongoClient

# os.environ["OPENAI_API_KEY"]= "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"

# pinecone.init(api_key="74dbb1f3-abda-4c51-8c24-3e600c7796f4",environment="gcp-starter")
# index = pinecone.Index("crewdogjobs")
# embedings= OpenAIEmbeddings(model="text-embedding-ada-002")
# # docsearch = Pinecone.from_existing_index(index,embedings)
# # print(len(docsearch.similarity_search("",k=3000)))

# # client=MongoClient("mongodb+srv://talhayasir:123fightfight@whiteboxscrapper.f0zx0xd.mongodb.net/?retryWrites=true&w=majority")
# client=MongoClient("mongodb+srv://shahbazkhan6732:AXkoh5XMDQBo3FyW@linkdin.q0omyf7.mongodb.net/?retryWrites=true&w=majority&appName=linkdin")
# db=client['job_scraper']
# linkedin_job=db["jobs"]

# def linkedin_automate(record):
#     print("----------------- in linkdin automate method----------------",record)

#     document = {
#             "metadata": {
#                 "job_title": record.get('position'),
#                 "job_source":record.get('job_source'),
#                 "job_id": record.get('job_id'),
#                 "job_status":record.get('job_status'),
#                 "location": record.get("location"),
#                 "hiring_person": record.get("hiring_person"),
#                 "text":str(record)
#             } }
#     keys_to_delete = [
#         "hiring_person_linkedin_link",
#         "other_information",
#         "job_id",
#         "search_keywords",
#         "time_stamp",
#         "job_status",
#         "_id",
        
#     ]

#     for i in keys_to_delete:
#         if 'search_keywords' in record:
#             if 'location' in record['search_keywords']:
#                 del record['search_keywords']['location']
#                 del record[i]

#     page_content = str(record)
#     metadata = document.get("metadata")
#     doc = Document(page_content=page_content, metadata=metadata)
#     doc_dict={
#             'vector': embedings.embed_query(doc.page_content),
#             'metadata': doc.metadata
#         }
    
#     if index.upsert(
#             vectors=[{
#                 'id': doc_dict.get("metadata").get("job_id"), 
#                 'values': doc_dict.get("vector"),
#                 'metadata': doc_dict.get("metadata")
#             }]
#         ):
#         return True
#     print("-----------------Exited from linkdin automate method----------------")
    






import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from pymongo import MongoClient
from pinecone import Pinecone as PineconeClient, ServerlessSpec

# Set environment variables
os.environ["OPENAI_API_KEY"] = "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"

# Initialize Pinecone
pc = PineconeClient(
    api_key="74dbb1f3-abda-4c51-8c24-3e600c7796f4"
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

# Connect to MongoDB
# client = MongoClient("mongodb+srv://talhayasir:123fightfight@whiteboxscrapper.f0zx0xd.mongodb.net/?retryWrites=true&w=majority")
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





# import pymongo
# import json
# import os
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.docstore.document import Document
# from langchain.vectorstores import Pinecone
# from pymongo import MongoClient
# import pinecone

# # Set environment variables
# os.environ["OPENAI_API_KEY"] = "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"

# # Initialize Pinecone
# pinecone.init(api_key="74dbb1f3-abda-4c51-8c24-3e600c7796f4", environment="us-west1-gcp")

# # Check if the index exists and create it if not
# if 'crewdogjobs' not in pinecone.list_indexes():
#     pinecone.create_index(
#         name='crewdogjobs',
#         dimension=1536,
#         metric='euclidean'
#     )

# index = pinecone.Index('crewdogjobs')
# embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# # Connect to MongoDB
# client = MongoClient("mongodb+srv://shahbazkhan6732:AXkoh5XMDQBo3FyW@linkdin.q0omyf7.mongodb.net/?retryWrites=true&w=majority&appName=linkdin")

# db = client['job_scraper']
# linkedin_job = db["jobs"]

# def linkedin_automate(record):
#     print("----------------- in linkdin automate method----------------", record)

#     document = {
#         "metadata": {
#             "job_title": record.get('position'),
#             "job_source": record.get('job_source'),
#             "job_id": record.get('job_id'),
#             "job_status": record.get('job_status'),
#             "location": record.get("location"),
#             "hiring_person": record.get("hiring_person"),
#             "text": str(record)
#         }
#     }
#     keys_to_delete = [
#         "hiring_person_linkedin_link",
#         "other_information",
#         "job_id",
#         "search_keywords",
#         "time_stamp",
#         "job_status",
#         "_id",
#     ]

#     for i in keys_to_delete:
#         if 'search_keywords' in record:
#             if 'location' in record['search_keywords']:
#                 del record['search_keywords']['location']
#                 del record[i]

#     page_content = str(record)
#     metadata = document.get("metadata")
#     doc = Document(page_content=page_content, metadata=metadata)
#     doc_dict = {
#         'vector': embeddings.embed_query(doc.page_content),
#         'metadata': doc.metadata
#     }

#     if index.upsert(
#             vectors=[{
#                 'id': doc_dict.get("metadata").get("job_id"),
#                 'values': doc_dict.get("vector"),
#                 'metadata': doc_dict.get("metadata")
#             }]
#     ):
#         return True

#     print("-----------------Exited from linkdin automate method----------------")
