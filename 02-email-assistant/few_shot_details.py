import json

class FewShotDetails:
    @staticmethod
    def get_examples():
        with open("data.json", "r") as file:
            data = json.load(file)
            examples = data["examples"]
        return examples

    @staticmethod
    def get_instructions():
        with open("data.json", "r") as file:
            data = json.load(file)
            prefix = data["instructions"]
        return prefix

    @staticmethod
    def get_example_template():
        template = """
        Email: {email_body}
        Response: {response}
        """
        example_variables = ["email_body", "response"]
        return template, example_variables


    @staticmethod
    def get_suffix():
        return """
                Email: {email_body}
                """
