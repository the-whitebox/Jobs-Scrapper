from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import os
import pinecone

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
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

vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embed,namespace="jobs",text_key='details')

