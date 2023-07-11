import openai
import pinecone

api_key="1dc22cc0-57e4-47c7-a364-3fd34c1ec992"
pinecone.init(api_key=api_key,environment='us-west4-gcp')

openai.api_key="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"

embed_model = "text-embedding-ada-002"
user_input = "crewdog imagine you are a heart doctor in London looking for a new job in Australia . I want to call or email a decision maker today . List only employers I can contact on the phone"

embed_query = openai.Embedding.create(
    input=user_input,
    engine=embed_model
)
#print(embed_query)
index_name='whitebox'
index=pinecone.Index(index_name)
# retrieve from Pinecone
query_embeds = embed_query['data'][0]['embedding']

# get relevant contexts (including the questions)
response = index.query(query_embeds, top_k=10, include_metadata=True,namespace='jobs')
# #print(response)
# for match in response['matches']:
#     print(f"{match['score']:.2f}\n:{match['metadata']['details']} \n :{match['metadata']['position']}")


query = "give me the job opportunities by this company 'https://www.linkedin.com/company/bmjcareers/'"

res = openai.Embedding.create(
    input=[query],
    engine=embed_model
)

# retrieve from Pinecone
xq = res['data'][0]['embedding']
res = index.query(xq, top_k=3, include_metadata=True,namespace="jobs")
print(res)
contexts = [item['metadata']['details'] for item in res['matches']]


augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query
# get relevant contexts (including the questions)
print(augmented_query)
res = index.query(xq, top_k=5, include_metadata=True,namespace="jobs")

primer = f"""You are CrewDog, a Q&A bot to find jobs. A highly intelligent system that answers
user questions based on the information provided by the user above
each question. If the information can not be found in the information
provided by the user you truthfully say "I don't know".
"""

res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "creata an answer for given context"},
        {"role": "user", "content": augmented_query}
    ]
)

print(res['choices'][0]['message']['content'])