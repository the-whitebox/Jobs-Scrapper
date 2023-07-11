from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain,RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.output_parsers import RegexParser
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

import os
import pinecone
os.environ["OPENAI_API_KEY"]="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"
os.environ["PINECONE_API_KEY"]="1dc22cc0-57e4-47c7-a364-3fd34c1ec992"
os.environ["PINECONE_API_ENV"]="us-west4-gcp"
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_API_ENV"]
)
index_name = "whitebox"

vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings,namespace="jobs")


qa = ConversationalRetrievalChain.from_llm(
    llm=OpenAI(temperature=0.6), 
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
    
    
)
chat_history = []
while True:

    query = input('prompt:')
    result = qa({"question": query, "chat_history": chat_history})

    print(result["answer"])
    print("----------------------------------------------------")
    print(result["source_documents"])


# prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

# {context}

# Question: {question}
# Answer in four lines:"""
# PROMPT = PromptTemplate(
#     template=prompt_template, input_variables=["context", "question"]
# )
# chain_type_kwargs = {"prompt": PROMPT}
# qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="map_reduce", retriever=vectorstore.as_retriever(),return_source_documents=True,chain_type_kwargs=chain_type_kwargs)

# query = "finding the psycharist jobs "
# # result=qa.run(query)
# # print(result)

# refine_prompt_template = (
#     "The original question is as follows: {question}\n"
#     "We have provided an existing answer: {existing_answer}\n"
#     "We have the opportunity to refine the existing answer"
#     "(only if needed) with some more context below.\n"
#     "------------\n"
#     "{context_str}\n"
#     "------------\n"
#     "Given the new context, refine the original answer to better "
#     "answer the question. "
#     "If the context isn't useful, return the original answer."
# )
# refine_prompt = PromptTemplate(
#     input_variables=["question", "existing_answer", "context_str"],
#     template=refine_prompt_template,
# )


# initial_qa_template = (
#     "Context information is below. \n"
#     "---------------------\n"
#     "{context_str}"
#     "\n---------------------\n"
#     "Given the context information and not prior knowledge, "
#     "answer the question: {question}\nYour answer should be precise.\n"
# )
# initial_qa_prompt = PromptTemplate(
#     input_variables=["context_str", "question"], template=initial_qa_template
# )
# chain = load_qa_chain(OpenAI(temperature=0), chain_type="refine", return_refine_steps=True,
#                      question_prompt=initial_qa_prompt, refine_prompt=refine_prompt)
# result=chain({"input_documents": vectorstore.similarity_search(query=query), "question": query}, return_only_outputs=True)
# print(result['output_text'])