from dotenv import load_dotenv
from few_shot import FewShot
from few_shot_utility import FewShotUtility

load_dotenv()


if __name__ == '__main__':
    examples = FewShot.get_examples()
    prefix = FewShot.get_prefix()
    suffix = FewShot.get_suffix()
    example_template, example_variables = FewShot.get_example_template()

    fewShot = FewShotUtility(examples=examples,
                                            prefix=prefix,
                                            suffix=suffix,
                                            input_variables=["email_body"],
                                            example_template=example_template,
                                            example_variables=example_variables
                                            )
    response = "Hello My name is Tony.   I am excited to be in the course.  I am hoping to learn about C++ programming.  I am a senior and this is my last class before I graduate."
    prompt = fewShot.get_prompt(response)
    email_response = fewShot.print_email_response(prompt)
    print(email_response)