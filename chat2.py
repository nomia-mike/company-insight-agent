"""
chat
by mike
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI()

system_prompt = (
    "You are a friendly and helpful Company Research Assistant. "
    "You provide prompt and accurate answers to all questions posed by your users. "
    "Today you will be working with a user to try to uniquely identify a company. "
    "You need to ask appropriate questions to help the user identify the company. "
    "Start by asking for the company's name. "
    "Note that the user may not know all of the information you request and that "
    "a company name rarely uniquely identifies a company. "
    "When you search the Internet for a company, you will often find companies "
    "with the same name. Estimate the number of possible matches and always supply that"
    "number in your response. An example of response you might give is:"
    "There are 5 possible matches to that name, can you let me know which country the company is in"
    "so that I can narrow the choices down?"
    "Once you have three or fewer option, provide a summary of these options in your response"
    "Your goal is to chat to the user and help them to uniquely identify a company."
)

def ask_chatgpt(history: list, user_message: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system", 
                "content": system_prompt
            },
            *history,
            {
                "role": "user", 
                "content": user_message
            }
        ],
        tools=[{"type": "web_search"}]  # enable web search
    )
    return response.output[0].content[0].text

def main():
    history = []
    print("Assistant: Hello! Which company are you looking for?")
    while True:
        try:
            msg = input("You: ").strip()
            if not msg:
                continue
            gpt_reply = ask_chatgpt(history, msg)
            print("Assistant:", gpt_reply)
            # update conversation history
            history.append({"role": "user", "content": msg})
            history.append({"role": "assistant", "content": gpt_reply})
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
