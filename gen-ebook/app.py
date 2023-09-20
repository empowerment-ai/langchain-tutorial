import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import json

# Load environment variables
load_dotenv()

# Initialize language model

llms = OpenAI(temperature=0.6, verbose=True, max_tokens=3500)

# Initialize Prompt Templates
prompt_template_title = PromptTemplate(
    input_variables=['topic'],
    template="You are an AI Assistant who is helping an author write an ebook about book about {topic}. I want you to generate a good title for such a book"
)

title_chain = LLMChain(llm=llms, prompt=prompt_template_title, output_key="title", verbose=True)

prompt_template_chapters = PromptTemplate(
    input_variables=['title', 'topic'],
    template="""
    I want you to create a complete outline for a book called {title} that is about {topic}.  The outlook should be as detailed as necessary.  
    All sub topics with the chapter should be completely defined as well. the output should be in JSON format.  Only return the JSON structure.
    the JSON structure should be a list of chapters.  Example JSON:
{{
   "chapters":[
      {{
         "title":"Introduction to Agile Methodologies",
         "subTopics":[
            {{
               "title":"What is Agile?",
               "subTopics":[
                  "History of Agile",
                  "Agile Principles and Values",
                  "The Agile Manifesto"
               ]
            }},
            {{
               "title":"Benefits of Agile Methodologies",
               "subTopics":[
                  "Increased Productivity",
                  "Better Quality",
                  "Faster Delivery",
                  "Improved Employee Engagement"
               ]
            }}
         ]
      }},
      {{
         "title":"Agile Methodologies and Practices",
         "subTopics":[
            {{
               "title":"Scrum",
               "subTopics":[
                  "Roles and Responsibilities",
                  "Scrum Events",
                  "Sprint Planning and Retrospective"
               ]
            }}
         ]
      }}
   ]
}}
    """
)

chapter_chain = LLMChain(llm=llms, prompt=prompt_template_chapters, output_key="book_chapters", verbose=True)

# New Prompt Template for Chapter Details
prompt_template_chapter_details = PromptTemplate(
    input_variables=['chapter_title', 'topic'],
    template="Please generate the detail text for a chapter in a book about '{topic}' entitled '{chapter_title}'.  Be sure to include as much detail as possible"
)

# New LLMChain for Chapter Details
chapter_details_chain = LLMChain(llm=llms, prompt=prompt_template_chapter_details, output_key="chapter_details", verbose=True)



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
        #st.write(response['book_chapters'])
        # Parse the JSON if it's a string
        if isinstance(response['book_chapters'], str):
            parsed_chapters = json.loads(response['book_chapters'])
        else:
            parsed_chapters = response['book_chapters']

        for i, chapter in enumerate(parsed_chapters['chapters']):
            st.write(f"Chapter {i + 1} - {chapter['title']}")
            for j, subtopic in enumerate(chapter['subTopics']):
                st.write(f"Subtopic {j + 1} - {subtopic['title']}")
            st.write("")

        for i, chapter in enumerate(parsed_chapters['chapters']):
            st.write(f"Generating details for Chapter {i + 1} - {chapter['title']}...")
            chapter_details_response = chapter_details_chain({'chapter_title': chapter['title'], 'topic': topic})
            st.write(f"Details for Chapter {i + 1} - {chapter['title']}:")
            st.write(chapter_details_response['chapter_details'])
            break  # remove break if you want details for all chapters

    else:
        st.write("Please enter a topic.")
