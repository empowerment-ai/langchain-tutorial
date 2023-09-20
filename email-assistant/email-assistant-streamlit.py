import streamlit as st
from email_few_shot import FewShot
from email_few_shot_utility import FewShotUtility
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
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
    st.title("Few-Shot Email Response Generator")
    response = st.text_area("Please enter your email:", 
                            "Hello My name is Tony. I am excited to be in the course. I am hoping to learn about C++ programming. I am a senior and this is my last class before I graduate.")
    
    if st.button("Generate Response"):
        prompt = fewShot.get_prompt(response)
        email_response = fewShot.print_email_response(prompt)
        st.write("Generated Email Response:")
        st.write(email_response)
