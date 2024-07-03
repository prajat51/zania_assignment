import openai
import fitz  # PyMuPDF
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class PDFQuestionAnsweringAgent:
#Initialize the PDFQuestionAnsweringAgent with the given PDF path, Slack token, and OpenAI API key.
    def __init__(self, pdf_path, slack_token, openai_api_key):
        self.pdf_path = pdf_path
        self.slack_token = slack_token
        self.openai_api_key = openai_api_key
        self.text_chunks = self.extract_text_from_pdf()

#Extract text from each page of the PDF and return a list of text chunks.
    def extract_text_from_pdf(self):
        text = ""
        document = fitz.open(self.pdf_path)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return self.chunk_text(text)

#Split the extracted text into chunks that are within the token limit.
    def chunk_text(self, text, max_tokens=9000):
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            word_length = len(word) + 1  # Add 1 for the space
            if current_length + word_length > max_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(word)
            current_length += word_length

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

# Query OpenAI with a chunk of text and a question, and return the response.

    def query_openai(self, text_chunk, question):
        openai.api_key = self.openai_api_key
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Answer the following question based on the content:\n\n{text_chunk}\n\nQuestion: {question}"}
                ],
                max_tokens=500
            )
            return response.choices[0].message['content'].strip()
        except openai.error.AuthenticationError as e:
            print(f"Authentication Error: {e}")
        except openai.error.OpenAIError as e:
            print(f"OpenAI Error: {e}")
        return None

#Post a message to a Slack channel.

    def post_to_slack(self, channel, message):
        client = WebClient(token=self.slack_token)
        try:
            response = client.chat_postMessage(channel=channel, text=message)
        except SlackApiError as e:
            print(f"Error posting to Slack: {e.response['error']}")

#Handle a question by querying OpenAI with each text chunk and posting the combined answer to Slack.
    def handle_question(self, channel, question):
        all_answers = []
        for chunk in self.text_chunks:
            answer = self.query_openai(chunk, question)
            if answer:
                all_answers.append(answer)
        all_answers=list(set(all_answers))
        print(all_answers)
        combined_answer = "\n\n".join(all_answers)
        self.post_to_slack(channel, combined_answer)

if __name__ == "__main__":
    pdf_path = "/content/handbook.pdf"
    #slack_token = os.getenv("xoxp-7384363864384-7361577031394-7365282756068-c9536ddc0d88073cd4146f927c6af88c")
    #os.environ['SLACK_TOKEN'] = 'xoxp-7384363864384-7361577031394-7365282756068-c9536ddc0d88073cd4146f927c6af88c'
    slack_token=os.environ['SLACK_TOKEN']
    #os.environ['OPENAI_API_KEY'] = 'sk-proj-4qjt5yH2ygyUWBycqSY8T3BlbkFJ0IbADr6q2yLdQ3ahmE2r'
    openai_api_key=os.environ['OPENAI_API_KEY']
    agent = PDFQuestionAnsweringAgent(pdf_path, slack_token, openai_api_key)
    question = ["What is the name of the company?",'Who is the CEO of the company?','What is their vacation policy?']
    channel = "#question-answering"
    for i in question:
      agent.handle_question(channel, i)
