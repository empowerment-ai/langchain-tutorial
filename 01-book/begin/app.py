import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import json
import time  # import the time module

# Load environment variables
load_dotenv()

# Streamlit UI
st.title('Generate Book')

