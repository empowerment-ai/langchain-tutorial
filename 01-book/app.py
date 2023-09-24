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

# Dropdown to select the model
model = st.selectbox('Select Model:', ['gpt-3.5-turbo', 'gpt-4'])

# Text input for the topic, style, and file name
topic = st.text_input('Enter the topic for the book:', '')

# Initialize language model
llms = ChatOpenAI(temperature=0.0, model=model)

# Initialize Prompt Templates with updated chapter and subtopic numbers
prompt_template_title = PromptTemplate(
    input_variables=['topic'],
    template="""You are an AI Assistant who is helping an author write an ebook about {topic}. Generate a good title for the book. 
    The book title should be no more than 10 words.
    """
)

title_chain = LLMChain(llm=llms, prompt=prompt_template_title, output_key="title")

prompt_template_chapters = PromptTemplate(
    input_variables=['title', 'topic'],
    template="""
    I want you to act as an expert on the topic of '{topic}'. I want you to an outline for a book called '{title}' for that topic.'
        
    """
)

chapter_chain = LLMChain(llm=llms, prompt=prompt_template_chapters, output_key="book_chapters")

prompt_template_chapter_count = PromptTemplate(
    input_variables=['book_chapters'],
    template="""
    I want you to give me just the number of chapters in this book based on the following table of contents:{book_chapters}.
    I only want the number of chapters, and nothing else.  For example, if there are 5 chapters, I want you to return JSON with the 
    following response: {{"chapters": "5"}}
    """
)

chapter_count_chain = LLMChain(llm=llms, prompt=prompt_template_chapter_count, output_key="chapter_count")

prompt_template_chapters_details = PromptTemplate(
    input_variables=['book_chapters', 'topic', 'chapter_number'],
    template="""
    I want you to act as an expert on the topic of '{topic}'. The TOC is {book_chapters}.  I want you write the chapter details for 
    chapter {chapter_number} of the book. I want the chapter broken down into the sub topics mentioned in the TOC for this chapter.  
    Each sub topic should be 3 to 5 paragrahs. I want you to write in a conversational tone.  I want you to write in a way that is
    easy to understand.  
    """
)

chapter_details_chain = LLMChain(llm=llms, prompt=prompt_template_chapters_details, output_key="chapter_details")

# Initialize the SequentialChain
chain = SequentialChain(
    chains=[title_chain, chapter_chain, chapter_count_chain],
    input_variables=["topic"],
    output_variables=["title", "book_chapters", 'chapter_count'],
)

# Initialize an empty string for accumulated_text outside the button callback
accumulated_text = ""

if st.button('Generate'):
    if topic:
        accumulated_text = ""
        
        st.text('Generating title...')
        response = title_chain({'topic': topic})
        
        st.subheader(f"Book Title: {response['title']}")
        accumulated_text += f"{response['title']}\n\n"
        
        st.text('Generating chapters...')
        response.update(chapter_chain({'topic': topic, 'title': response['title']}))
        
        st.subheader("Table Of Contents")
        st.write(response['book_chapters'])
        accumulated_text += "================Table Of Contents======================\n"
        accumulated_text += f"{response['book_chapters']}\n\n"
        
        response.update(chapter_count_chain({'book_chapters': response['book_chapters']}))
        parsed_chapter_count = json.loads(response['chapter_count'])
        num_chapters = int(parsed_chapter_count['chapters'])
        st.text(f"Number of chapters: {num_chapters}")
        
        # Initialize the progress bar with value 0
        progress_bar = st.progress(0)
        
        for chapter in range(num_chapters):
            st.text(f"Generating details for Chapter {chapter+1}...")
            chapter_details_response = chapter_details_chain({'book_chapters': response['book_chapters'], 
                                                              'topic': topic, 
                                                              'chapter_number': chapter+1})
            chapter_details = chapter_details_response['chapter_details']
            word_count = len(chapter_details.split())
            st.write(f"Chapter {chapter+1} Word Count: {word_count}")
            accumulated_text += f"Chapter {chapter+1}\n"
            accumulated_text += f"{chapter_details}\n\n"
            
            # Update the progress bar for each chapter generated
            progress = (chapter + 1) / num_chapters
            progress_bar.progress(progress)
            time.sleep(0.1)  # You can remove this line, it’s just for visual effect
            
        # Display the accumulated text in a single text area
        st.text_area('Generated Content:', accumulated_text, height=2000)
        
        # Reset the progress bar to 0 once generation is complete
        progress_bar.progress(0)
        
        st.success('Generation Complete!')
        # After generating the content...
        st.download_button('Download Generated Content', accumulated_text, 'generated_content.txt')

    else:
        st.error("Please enter a topic")
