import pytest
from packages.ai_chatbot import chatbot

def test_chatbot():
    assert chatbot('Give only the answer for 1+1') == '2'

