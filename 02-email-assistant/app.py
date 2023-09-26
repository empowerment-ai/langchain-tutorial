import streamlit as st
from email_few_shot import FewShot
from email_few_shot_utility import FewShotUtility
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == '__main__':
    st.set_page_config(page_title="Email Assistant")
    st.header('🦜🔗 Email Assistant')
    
    openai_api_key_env = os.getenv('OPENAI_API_KEY')
    openai_api_key = st.sidebar.text_input('OpenAI API Key', placeholder='sk-', value=openai_api_key_env)

    examples = FewShot.get_examples()
    prefix = FewShot.get_prefix()
    suffix = FewShot.get_suffix()
    example_template, example_variables = FewShot.get_example_template()

    fewShot = FewShotUtility(
        examples=examples,
        prefix=prefix,
        suffix=suffix,
        input_variables=["email_body"],
        example_template=example_template,
        example_variables=example_variables
    )

    # Streamlit UI
    st.title("Email Response Generator")
    

    with st.form('my_form'):
        model = st.selectbox('Select Model:', ['gpt-3.5-turbo', 'gpt-4'])
        response = st.text_area("Please enter your email:", "")

        submitted = st.form_submit_button('Generate')
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
        if submitted and openai_api_key.startswith('sk-'):
            prompt = fewShot.get_prompt(response)
            email_response = fewShot.print_email_response(openai_api_key, prompt )
            st.write("Generated Email Response:")
            st.write(email_response)

