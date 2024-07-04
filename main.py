import os
from pdf_question_answering_agent import PDFQuestionAnsweringAgent

if __name__ == "__main__":
    pdf_path = "path/to/your/pdf/handbook.pdf"
    slack_token=os.environ['SLACK_TOKEN']
    openai_api_key=os.environ['OPENAI_API_KEY']

    agent = PDFQuestionAnsweringAgent(pdf_path, slack_token, openai_api_key)
    
    questions = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?"
    ]
    
    channel = "#question-answering"
    
    for question in questions:
        agent.handle_question(channel, question)
