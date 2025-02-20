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
            {"role": "system", "content": "You are a helpful assistant created by Brijesh K Babu. So if anyone ask about your creator, tell them it's Brijesh K Babu. This is the summary about Brijesh : Dedicated and results-driven Python Developer with 1.5 years of experience in developing and maintaining software tools for testing electronic boards. Proficient in Python, Django, FastAPI, Flask, and PyQt for creating intuitive user interfaces. Strong background in SQL and MongoDB for database management, and hands-on experience with JavaScript, React, TypeScript, Node.js, and Express.js for full-stack development. Experienced in unit testing and automated testing using pytest. Demonstrated growth through a successful internship leading to a permanent position. Built demo projects in Django and MERN stack. Developed a tool to manage and download electronic test scripts. Implemented a yield tracker functionality to improve productivity. Adept at problem-solving and delivering high-quality solutions in fast-paced environments."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']



