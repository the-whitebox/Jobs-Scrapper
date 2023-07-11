from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from tqdm.autonotebook import tqdm
import pinecone
import openai
Openai_api_key="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"

api_key="1dc22cc0-57e4-47c7-a364-3fd34c1ec992"
Index_name="whitebox"
Name_space="qcs_doc"
model_name='text-embedding-ada-002'
pinecone.init(api_key=api_key,environment='us-west4-gcp')
pdfs=["/home/whitebox/sementic_search/documents/A guide to launching a domiciliary care agency - Scotland.pdf",
      "/home/whitebox/sementic_search/documents/Adverse Weather Driving Tips.pdf",
      "/home/whitebox/sementic_search/documents/Autumn COVID-19 Booster Plan Agreed by Government.pdf",
      "/home/whitebox/sementic_search/documents/Barriers to Realising Human Rights for People Living with Dementia in Care Homes.pdf",
      "/home/whitebox/sementic_search/documents/Brexit and immigration in the UK.pdf",
      "/home/whitebox/sementic_search/documents/Building a Better Workforce Survey Our Findings.pdf",
      "/home/whitebox/sementic_search/documents/Diet and Nutrition Advice.pdf"]
annual_reports = []
for pdf in pdfs:
    loader = PyPDFLoader(pdf)
    # Load the PDF document
    document = loader.load()        
    # Add the loaded document to our list
    annual_reports.append(document)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)

chunked_annual_reports = []
for annual_report in annual_reports:
    # Chunk the annual_report
    texts = text_splitter.split_documents(annual_report)
    # Add the chunks to chunked_annual_reports, which is a list of lists
    chunked_annual_reports.append(texts)
    print(f"chunked_annual_report length: {len(texts)}")
    print(texts)
embeddings=OpenAIEmbeddings(openai_api_key=Openai_api_key)

for chunks in chunked_annual_reports:
    Pinecone.from_texts([chunk.page_content for chunk in chunks], embeddings, index_name=Index_name,namespace=Name_space)

index=pinecone.Index(Index_name)
print('Index status-------------------------',index.describe_index_stats())