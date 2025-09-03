"""
insight-agent
by mike
"""
# pylint: disable=import-error

#import os
from dotenv import load_dotenv
#from openai import OpenAI #

load_dotenv(override=True)

client = OpenAI()

SYSTEM_PROMPT = (
    "You are an efficient Research Assistant. "
    "You are provided with information that identifies a company. "
    "You will search the web for information about that company"
    "and produce a report of between 10 and 20 paragraphs in plain English." 
)

"""
def research() -> str:
    Uses OpenAI's responses API to interactively ask ChatGPT a question
    and returns the answer as a string.
    
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
        tools=[{"type": "web_search"}]  # enable web search
    )
    return response.output[0].content[0].text
"""

def main():
    """
    Main function
    """
    print("Arguments passed into main():")
    for i, arg in enumerate(sys.argv):
        print(f"argv[{i}] = {arg}") 

if __name__ == "__main__":
    main()
