from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import pinecone
import os
import time


os.environ["PINECONE_API_KEY"]="1dc22cc0-57e4-47c7-a364-3fd34c1ec992"
os.environ["PINECONE_API_ENV"]="us-west4-gcp"
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_API_ENV"]
)
os.environ["OPENAI_API_KEY"]="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"
# embeddings = OpenAIEmbeddings()
# index_name="whitebox"
# vectorstore = Pinecone.from_documents(index_name=index_name, embedding=embeddings,namespace="jobs")

# print(vectorstore.as_retriever())
# qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="map_reduce", retriever=vectorstore.as_retriever())
# query = "doctors jobs in london "
# result=qa.run(query)
# print(result)

# llm = OpenAI(temperature=0)
# conversation = ConversationChain(
#     llm=llm, verbose=True, memory=ConversationBufferMemory()
# )


# template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

# Current conversation:
# {history}
# Human: {input}
# AI Assistant:"""
# PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
# conversation = ConversationChain(
#     prompt=PROMPT,
#     llm=llm,
#     verbose=True,
#     memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
# )
# q=["hi","what is weather"]
# while True:
#     text=input("prompt")
#     print(conversation.predict(input=text))
#     time.sleep(5)



# condensed_question_prompt = PromptTemplate(
#     template="Given the context: {context}, what is the {question_type}?",
#     input_variables=["context", "question_type"]
# )
# template=''''this is a conversation about job search'''
# # Generate a condensed question prompt using the template
# context = "The article discusses the benefits of exercise for mental health."
# question_type = "main conclusion"
# prompt = PromptTemplate.format(template)
# chain_type_kwargs = {"prompt": prompt}
# #print(prompt)





index_name="whitebox"
model_name = 'text-embedding-ada-002'
embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)
promt="you are intelliegnt QA assiatant to search jobs in given context"
llm = ChatOpenAI(
    openai_api_key="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",
    model_name='gpt-3.5-turbo',
    temperature=1,
    
    
    
)

#chain_type_kwargs = {"prompt": prompt}
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embed,namespace="qcs_docs",text_key='text')
qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory,chain_type="stuff")



print(qa.get_chat_history)
while True:
    text=input("prompt:")
    result = qa({"question": text})
    print(result["answer"])
    