import os
import pinecone
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
import os
from dotenv import load_dotenv

load_dotenv()

model_name = "gpt-3.5-turbo"
openai_api_key_env = os.getenv('OPENAI_API_KEY')
pinecone_api_key_env = os.getenv('PINECONE_API_KEY')

llm = ChatOpenAI(openai_api_key=openai_api_key_env,  model=model_name)
chain = load_qa_chain(llm, chain_type="stuff")
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
pinecone.init(api_key=pinecone_api_key_env, environment='gcp-starter')
index = Pinecone.from_existing_index('langchain-demo', embeddings)

def get_similiar_docs(query, k=5):
    similar_docs = index.similarity_search(query, k=k)
    print(similar_docs)
    return similar_docs

def get_answer(query):
  similar_docs = get_similiar_docs(query)
  answer = chain.run(input_documents=similar_docs, question=query)
  return answer

while True:
  query = input("\n\nWhat is your question? \n")
  answer = get_answer(query)
  print(f'\n\n\n{answer}\n\n\n')