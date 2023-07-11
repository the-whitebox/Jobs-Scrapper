
from langchain.prompts import StringPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.vectorstores import FAISS,Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.llms import OpenAI
from langchain.chains.router import MultiPromptChain
from langchain.llms import OpenAI
from langchain.chains.router import MultiRetrievalQAChain
import os 
import pinecone
os.environ["PINECONE_API_KEY"]="1dc22cc0-57e4-47c7-a364-3fd34c1ec992"
os.environ["PINECONE_API_ENV"]="us-west4-gcp"
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_API_ENV"]
)
#os.environ["OPENAI_API_KEY"]="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"
# Jobs_template = """Your name is CrewDog and you are an AI assistant to find the jobs. \
# You have your own database and you have to find the jobs from your own database.\
# When you don't know the answer try to find the answer from database.

# Here is a question:
# {input}"""


# doc_templates = """You are CrewDog and you are an AI assistant to find the documents from QCS \
# answer the component parts, and then put them together to answer the broader question.

# Here is a question:
# {input}"""

# prompt_infos = [
#     {
#         "name": "job search", 
#         "description": "Good for finding jobs", 
#         "prompt_template": Jobs_template
#     },
#     {
#         "name": "documents search", 
#         "description": "Good for finding the answers from qcs documents", 
#         "prompt_template": doc_templates
#     }
# ]
# chain = MultiPromptChain.from_prompts(OpenAI(), prompt_infos, verbose=True)
# print(chain.run("I am doctor and finding job?"))
# print(chain.run("I am finding policies. who are you?"))
# print(chain.run("What is the name of the type of cloud that rins"))
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts import PromptTemplate

model_name = 'text-embedding-ada-002'
os.environ["OPENAI_API_KEY"]="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"
embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)
index_name = "whitebox"
# q="tell me dataile about qualified doctors  "
vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embed,namespace="jobs",text_key="details")
# print(vectorstore)
# re=vectorstore.similarity_search(
#     query=q,  # our search query
#     k=3  # return 3 most relevant docs
# )
# for i in re:
#     print("----------------------------------",i,"----------------------------")
     
# chat completion llm
llm = ChatOpenAI(
    openai_api_key="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",
    model_name='gpt-3.5-turbo',
    temperature=0.5,
)
# conversational memory
conversational_memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,
    return_messages=True
)
# retrieval qa chain
prompt_template = """You are CrewDog an intelligent QA aisstant to find the jobs.Try to find the jobs in given contaxt. your contaxt is your database.If you do not find the job try to collect more information of the job seeker.

{context}

Question: {question}
Answer :"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs=chain_type_kwargs,

    
    
   
)
while True:
    q=input('prompt:')
    postfix=""
    query=str(q+postfix)
    re=qa.run(query)
    print(re)
    print(type(re))

tools = [
    Tool(
        name='Knowledge Base',
        func=qa.run,
        description=(
            'The tool is an intelligent QA assistant named crewdog '
            'more information about the topic'
        )
    )
]
agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory
)
# q=["who are you?","I am a doctor and finding jobs in london","show me detail descriptions for given jobs "]
# for q in q:
#     re=qa.run(q)
#     print(re)
#     result=agent(q)
#     print(result)     