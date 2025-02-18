import pytest
from packages.ai_chatbot import chatbot


def test_chatbot():
    try:
        response = chatbot('Give only the answer for 1+1')
    except:
        response = 'Error from ai_chatbot'
    assert response == '2'
