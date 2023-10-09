import os
import pinecone 
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv

load_dotenv()

directory = './data'

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

documents = load_docs(directory)
for document in documents:
  print(document.metadata)
print(len(documents))

def split_docs(documents,chunk_size=500,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),  # find at app.pinecone.io
    environment="gcp-starter"  # next to api key in console
)

index_name = "langchain-demo"
index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
print(f'Documents indexed and stored to pinecone. (Vector Count: {len(docs)})')