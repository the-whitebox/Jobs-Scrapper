import pinecone
import pinecone.info
import openai
from data_prepation import *
from tqdm.auto import tqdm
import pickle
api_key="1dc22cc0-57e4-47c7-a364-3fd34c1ec992"
pinecone.init(api_key=api_key,environment='us-west4-gcp')

version_info=pinecone.info.version()

server_version=".".join(version_info.server.split(".")[:2])
client_version=".".join(version_info.client.split(".")[:2])


print("Index Creating-----------")
index_name='whitebox'
with open('embeddings.pkl','rb') as embeddings:
    chunks=pickle.load(embeddings)

print(type(chunks))
print(chunks)   
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name,dimension=1536,metric='cosine')

index=pinecone.Index(index_name)
print(index.describe_index_stats())
print("Index Created-----------------",index_name)
batch_size=500


for i in tqdm(range(0, len(list(chunks['details'])), batch_size)):
    print(i)
    i_end = min(len(list(chunks)), i+batch_size)
    meta_batch = chunks[i:i_end]
    ids_batch = [x['job_id'] for x in meta_batch]
    embeds = [x['embeddings'] for x in meta_batch]
    meta_batch = [{
        'position': x['position'],
        'details': x['details'],
        'company': x['company'],
        'location':x['location'],
        'job_source':x['job_source'],
        'hiring_person':x['hiring_person'],
        'job_id':x['job_id']
    } for x in meta_batch]
    to_upsert = list(zip(ids_batch,embeds, meta_batch))
    index.upsert(vectors=to_upsert,namespace='jobs')

index=pinecone.Index(index_name)
print('Index status-------------------------',index.describe_index_stats())



