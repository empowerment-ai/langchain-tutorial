class FewShot:

    @staticmethod
    def get_examples():
        examples = [
            {
                "email_body": """Hello Everyone my name is Bob and I’m excited to learn more about Python programming. 
                This is my last class before I complete my associate degree. I currently work full time at Verizon doing IT support and my major is Cyber Security. 
                My expectation of this course is to just learn and be sponge on everything this course has to be offer because I know this will help in my career as 
                far as being a cyber security professional.""",
                "response": """
                Bob, Welcome to the course.  It is a pleasure to meet you. Looking forward to working with you this fall.  Congrats on being so close to finishing your
                degree.  I always excited when I see students working towards a Cyber degree. As you know its in great demand.  Please stay on track with 
                assignments and due date.  And feel free to reach out if you ever need any help or struggle in any way.  
                Cheers, Prof Michak
                """
            },
            {
                "email_body": """
                1) This is my first online college level class.
                2) I am a sophomore in college and about 30% done with my degree. 
                3) My major is Computer Science.
                4) From this course, I am expecting to be able to write a code and debug it in the Python language. 
                I am hoping that I will be able to resolve issues and simplify processes with the use of this language. 

                Good luck with this course everyone!
                """,
                "response": """
                Paula, Great to meet you and welcome to the course.  I am really excited to get started.  This course will definately teach you the fundamentals of 
                C++.   All due dates are posted.  It is important to stay on track in order to have the best chance to do well in this course.
                Please reach out if you have questions or need help along the way.  
                Cheers, Prof Michak
                """
            },
            {
                "email_body": """
                My name is Michael and this is not my first online class. I am in my final semester here and will be transferring in the spring. 
                I have worked my entire adult life in healthcare, particularly the Emergency Medical side. 
                My long term goal is to stay in healthcare but work cyber security ensuring patient safety from the IT realm. 
                I expect to learn the basics of Python and hope that this will peak my interest in coding and allow me to add a new skill to my resume.
                """,
                "response": """
                        Michael,  Its nice to meet you.  Welcome to the course.   I see there is light at the end of the tunnel for you. 
                        Excellent choice in choosing Cyber, and your associate degree.  Cyber is a great major. Best of luck this
                        semester.  If you need any help or have questions, please reach out.
                        Cheers, Prof Michak
                        """
            }
        ]
        return examples

    @staticmethod
    def get_example_template():
        template = """
        Email: {email_body}
        Response: {response}
        """
        example_variables = ["email_body", "response"]
        return template, example_variables

    @staticmethod
    def get_prefix():
        return f"""
        I want you to play the role of a IA asistant helping to answer emails for new students in a course.  Your responses should be no more than 3 or 4 sentences
        and in my writing style.  If the student provided their name, you should address them within the response.  Be sure to welcome them and remind them 
        to always reach out for help if they struggle. It should be in a friendly tone as well.  If the student mentions working or having a family, be sure to 
        encourage them and let them know that you understand the difficulting balancing work and or life and school.    
        """

    @staticmethod
    def get_suffix():
        return """
                Email: {email_body}
                """
