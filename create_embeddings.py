import openai
import json
import pickle

from data_prepation import *
openai.api_key="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"

sample_data=final_datafram()
print(sample_data)

#create embeddings

print("Embedds creating")
sample_data['embeddings']=sample_data.details.apply(lambda x:openai.Embedding.create(input=x,engine='text-embedding-ada-002')['data'][0]['embedding'])

print("embeds ceated successfuly")
print(sample_data.head())
chunks=sample_data.to_dict(orient='records')
print(chunks,type(chunks))
try:
    
    with open('embeddings.pkl','wb') as embeddings:
        pickle.dump(chunks,embeddings)
    print("File saved")
except:
    print("File not saved")

