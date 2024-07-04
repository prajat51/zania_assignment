import openai

class OpenAIQuery:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key

    def query(self, text_chunk, question):
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
