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

def ask_chatgpt(history: list) -> str:

    response = client.responses.create(
        model="gpt-4o-mini",
        input=history,
        instructions=system_prompt,
        tools=[{"type": "web_search"}]
    )
    return response
#    return response.output[0].content[0].text

user_prompt = "Which company are you looking for?:"
history = [
    {
        "role": "user",
        "content": user_prompt
    }
]

while True:
    try:
        msg = input(f"{user_prompt} ").strip()
        if not msg: 
            continue
        gpt_response = ask_chatgpt(history)
        
    except (EOFError, KeyboardInterrupt):
        print("\nbye!")
        sys.exit(0)

    user_prompt = "> "
    text_response = gpt_response.output[0].content[0].text
    print(f"response was: {text_response}")
    history += [{"role": el.role, "content": el.content} for el in gpt_response.output]
    history.append({ "role": "user", "content": user_prompt })


