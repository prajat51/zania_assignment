from pdf_extractor import PDFExtractor
from openai_query import OpenAIQuery
from slack_notifier import SlackNotifier

class PDFQuestionAnsweringAgent:
    def __init__(self, pdf_path, slack_token, openai_api_key):
        self.pdf_extractor = PDFExtractor(pdf_path)
        self.openai_query = OpenAIQuery(openai_api_key)
        self.slack_notifier = SlackNotifier(slack_token)
        self.text_chunks = self.pdf_extractor.chunk_text(self.pdf_extractor.extract_text_from_pdf())

    def handle_question(self, channel, question):
        all_answers = []
        for chunk in self.text_chunks:
            answer = self.openai_query.query(chunk, question)
            if answer:
                all_answers.append(answer)
        all_answers = list(set(all_answers))
        combined_answer = "\n\n".join(all_answers)
        self.slack_notifier.post_message(channel, combined_answer)
