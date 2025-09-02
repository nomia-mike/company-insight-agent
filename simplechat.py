#!/usr/bin/env python
# coding: utf-8

# 
# ### test of the Responses API
# 

import os, sys
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI()

system_prompt = f"You are a friendly and helpful Company Research Assistant. \
    You provide prompt and accurate answers to all questions posed by your users. \
    Today you will be working with a user to try to uniquely identify a company. \
    You need to ask appropriate questions to help the user identify the company. \
    Start by asking a for the company's name.\
    Note that the user may not know all of the information you request and that \
    a company name rarely uniquely identifies a company.\
    When you search the Internet for a company, you will often find companies with the same name.\
    You will need to ask additional questions to help the user identify the company.\
    Your goal is to chat to the user and help them to uniquely identify a company."

def ask_chatgpt(user_text: str) -> str:

    response = client.responses.create(
        model="gpt-4o-mini",
        input="user_text",
        instructions=system_prompt,
        tools=[{"type": "web_search"}]
    )
    return response.output[0].content[0].text


while True:
    try:
        msg = input("you: ").strip()
        if not msg: 
            continue
        print("assistant:", ask_chatgpt(msg))
    except (EOFError, KeyboardInterrupt):
        print("\nbye!")
        sys.exit(0)

