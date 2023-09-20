import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# Load environment variables
load_dotenv()

# Initialize language model
llms = OpenAI(temperature=0.6)

# Initialize Prompt Templates
prompt_template_title = PromptTemplate(
    input_variables=['topic'],
    template="You are an AI Assistant who is helping an author write an ebook about book about {topic}. I want you to generate a good title for such a book"
)

title_chain = LLMChain(llm=llms, prompt=prompt_template_title, output_key="title")

prompt_template_chapters = PromptTemplate(
    input_variables=['title', 'topic'],
    template="I want you to create a list of chapters for a book called {title} that is about {topic}"
)

chapter_chain = LLMChain(llm=llms, prompt=prompt_template_chapters, output_key="book_chapters")

# New Prompt Template for Chapter Details
prompt_template_chapter_details = PromptTemplate(
    input_variables=['chapter_title', 'topic'],
    template="Please generate the detail text for a chapter in a book about '{topic}' entitled '{chapter_title}'.  Be sure to include as much detail as possible"
)

# New LLMChain for Chapter Details
chapter_details_chain = LLMChain(llm=llms, prompt=prompt_template_chapter_details, output_key="chapter_details")



# Initialize the SequentialChain
chain = SequentialChain(
    chains=[title_chain, chapter_chain],
    input_variables=["topic"],
    output_variables=["title", "book_chapters"]
)

# Streamlit UI
st.title('Generate Book')

# Text input for the topic
topic = st.text_input('Enter the topic for the book:', '')

# Button to generate the title and chapters
if st.button('Generate'):
    if topic:
        response = chain({'topic': topic})
        st.write(f"Generated Book Title: {response['title']}")
        st.write("List of Chapters:")
        st.write(response['book_chapters'])

        # Generate details for each chapter
        for i, chapter in enumerate(response['book_chapters'].split("\n")):  # Assuming chapters are separated by newlines
            chapter_details_response = chapter_details_chain({'chapter_title': chapter, 'topic': topic})
            st.write(f"Details for Chapter {i + 1} - {chapter}:")
            st.write(chapter_details_response['chapter_details'])
            break
    else:
        st.write("Please enter a topic.")
