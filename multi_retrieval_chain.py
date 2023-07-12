from langchain.chains.router import MultiRetrievalQAChain
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import SimpleSequentialChain



from langchain.llms import OpenAI
import os
import pinecone

os.environ["PINECONE_API_KEY"]="1dc22cc0-57e4-47c7-a364-3fd34c1ec992"
os.environ["PINECONE_API_ENV"]="us-west4-gcp"
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_API_ENV"]
)
os.environ["OPENAI_API_KEY"]="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"

index_name="whitebox"
model_name = 'text-embedding-ada-002'
embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)
vectorstore_jobs = Pinecone.from_existing_index(index_name=index_name, embedding=embed,namespace="jobs",text_key='details').as_retriever()
vectorstore_qcs = Pinecone.from_existing_index(index_name=index_name, embedding=embed,namespace="qcs_doc",text_key='text').as_retriever()

llm = ChatOpenAI(
    openai_api_key="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",
    model_name='gpt-3.5-turbo',
    temperature=1
)
jobs_chain= RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=vectorstore_jobs)
doc_chain= RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=vectorstore_qcs)
job_template = """You are a very smart AI assistant . \
You are great at finding jobs only in given context and out of context. \
if you find the hiring manager details please mention otherwise do not mention. \
if you find any recuriter information please mention except job sources. \
When you don't know the answer don't say "I don't know" try to make the relevent answer out of contaxt. \
Do not appologize just create a smart answer.

{context}
Question:{question}
Answer:
"""


doc_template = """An smart AI assisatnt to create an answer in the given context. \


{context}
Question:{question}
Answer"""
job_prompt=PromptTemplate(template=job_template,input_variables=["context","question"])
doc_prompt=PromptTemplate(template=doc_template,input_variables=["context","question"])
retriever_infos = [
    {
        "name": "Job search", 
        "description": "intelligent assistant to find jobs", 
        "retriever": vectorstore_jobs,
        "prompt": job_prompt
    },
    {
        "name": "document search", 
        "description": "intelligent assistant for Q&A in given context", 
        "retriever": vectorstore_qcs,
        "prompt": doc_prompt
    },

    
]
 
chain = MultiRetrievalQAChain.from_retrievers(llm, retriever_infos,verbose=True)
#overall_chain = SimpleSequentialChain(chains=[jobs_chain, doc_chain], verbose=True)

while True:
    text=input("prompt:")
    result = chain.run(text)
    print(result)
    print(type(result))