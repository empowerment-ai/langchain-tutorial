import streamlit as st
from few_shot_details import FewShotDetails
from few_shot_utility import FewShotUtility
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == '__main__':
    st.set_page_config(page_title="Email Assistant")
    st.header('🦜🔗 Email Response Generator')
    
    openai_api_key_env = os.getenv('OPENAI_API_KEY')
    openai_api_key = st.sidebar.text_input('OpenAI API Key', placeholder='sk-', value=openai_api_key_env)

    examples = FewShotDetails.get_examples()
    instructions = FewShotDetails.get_instructions()
    suffix = FewShotDetails.get_suffix()
    example_template, example_variables = FewShotDetails.get_example_template()

    fewShot = FewShotUtility(
        examples=examples,
        prefix=instructions,
        suffix=suffix,
        input_variables=["email_body"],
        example_template=example_template,
        example_variables=example_variables
    )
    with st.form('my_form'):
        #model = st.selectbox('Select Model:', ['gpt-3.5-turbo', 'gpt-4'])
        response = st.text_area("Please enter the body of a recieved email:", "")

        submitted = st.form_submit_button('Generate')
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
        if submitted and openai_api_key.startswith('sk-'):
            prompt = fewShot.get_prompt(response)
            email_response = fewShot.generate_email_response(openai_api_key, prompt )
            st.write("Generated Email Response:")
            st.write(email_response)

