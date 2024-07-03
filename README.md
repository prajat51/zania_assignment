# zania_assignment
# PDF Question Answering Agent
This script extracts text from a PDF document, uses OpenAI's GPT-3.5-turbo-0125 model to answer specific questions based on the content, and posts the answers to a Slack channel.

# Dependencies:
openai: To interact with the OpenAI API.\
PyMuPDF (imported as fitz): To handle PDF extraction.\
slack_sdk: To interact with the Slack API.

# Setup:
1.Install the necessary Python packages:\
pip install openai pymupdf slack_sdk\
2 Set the environment variables for your Slack API token and OpenAI API key:\
export SLACK_TOKEN='your-slack-token'\
export OPENAI_API_KEY='your-openai-api-key'\

# Usage:
Update the pdf_path variable with the path to your PDF document.\
Update the channel variable with the Slack channel where you want to post the answers.\
Add your questions to the questions list.
