"""
chat-agent
by mike
"""
# pylint: disable=import-error

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI()

SYSTEM_PROMPT = (
    "You are a friendly and helpful Company Research Assistant. "
    "You provide prompt and accurate answers to all questions posed by your users. "
    "Today you will be working with a user to try to uniquely identify a company. "
    "You need to ask appropriate questions to help the user identify the company. "
    "Start by asking for the company's name. "
    "Note that the user may not know all of the information you request and that "
    "a company name rarely uniquely identifies a company. "
    "When you search the Internet for a company, you will often find companies "
    "with the same name. Estimate the number of possible matches and always supply that"
    "number in your response. "
    "Once you have three or fewer option, provide a summary of these options in your response."
    "Once you have only one option, then use the function tool named 'insight' to produce a report on that company."
    "Only use the function tool named 'insight' when you are down to exactly one option"
    "Your goal is to chat to the user and help them to uniquely identify a company."
)

tools = [
    {"type": "web_search"},
    {
        "type": "function",
        "name": "insight",
        "description": "Provide detailed report about given company.",
        "parameters": {
            "type": "object",
            "properties": {
                "website": {
                    "type": "string",
                    "description": "The company's website URL"
                },
                "company_name": {
                    "type": "string",
                    "description": "The official name of the company"
                },
                "country": {
                    "type": "string",
                    "description": "The country where the company is located"
                }
            }
        }
    }
]

def ask_chatgpt(history: list, user_message: str):
    """
    Uses OpenAI's responses API to interactively ask ChatGPT a question
    and returns the answer as a string.
    """
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system", 
                "content": SYSTEM_PROMPT
            },
            *history,
            {
                "role": "user", 
                "content": user_message
            }
        ],
        tools=tools
    )
    #print(f"response type is {type(response)}")
    return response

def insight(website: str, company_name: str, country: str) -> str:
    company_name = "nomia"
    return f"da comapny called {company_name} is gud."

def main():
    """
    Main function
    Asks the user questions in a loop in order to find the company they are looking for
    """
    history = []
    print("Assistant: Hello! Which company are you looking for?")
    while True:
        try:
            msg = input("You: ").strip()
            if not msg:
                continue
            #print(f"calling chatgpt with msg: {msg}")
            gpt_reply = ask_chatgpt(history, msg)
            mytype = type(gpt_reply)
            #print(f"returned with something of type {mytype}")
            for item in gpt_reply.output:
                if item.type == "function_call":
                    company_detail = json.loads(item.arguments)
                    result = insight(company_detail['website'],company_detail['company_name'],company_detail['country'])
                    company_report = json.dumps(result)
                    print(f"Here is the result {company_report}")
                    os._exit(0)
            #gpt_response_text = gpt_reply[0].content[0].text
            print(f"Assistant: {gpt_reply.output_text}")
            history.append({"role": "user", "content": msg})
            history.append({"role": "assistant", "content": gpt_reply.output_text})
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
