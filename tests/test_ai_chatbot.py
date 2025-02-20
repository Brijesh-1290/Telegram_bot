import pytest
from packages.ai_chatbot import chatbot
chat = [
    {"role": "system",
     "content": "You are a helpful ai assistant"}
]

def test_chatbot():
    global chat
    convo = chat
    convo.append({"role":"user",
                 "content":"Give only the answer for 1+1"})
    try:
        response = chatbot(convo)
    except:
        response = 'Error from ai_chatbot'
    assert response == '2'
