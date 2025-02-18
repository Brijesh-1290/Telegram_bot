import openai
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Access an environment variable
api_key = os.getenv('OPEN_AI_API_KEY')
# Initialize the OpenAI client
openai.api_key = api_key


def chatbot(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']



