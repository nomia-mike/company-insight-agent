"""
insight_agent
by mike
"""
# pylint: disable=import-error

import sys
from dotenv import load_dotenv
from openai import OpenAI #

load_dotenv(override=True)

client = OpenAI()

SYSTEM_PROMPT = (
    "You are an efficient Research Assistant. "
    "You are provided with the name, web site and country for a company. "
    "You will search the web for information about that company"
    "and produce a report of between 10 and 20 paragraphs in plain English." 
)


def research(website: str, company_name: str, country: str) -> str:
    """
    Uses OpenAI's responses API to interactively ask ChatGPT a question
    and returns the answer as a string.
    """
    user_message = f"The company name is {company_name} \
                    their web site is {website} \
                    and they are located in {country}"
    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "system", 
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user", 
                "content": user_message
            }
        ],
        tools=[{"type": "web_search"}]
    )
    return response

def main():
    """
    Main function
    """
    report = research(sys.argv[1], sys.argv[2], sys.argv[3]).output_text
    print(report)

if __name__ == "__main__":
    main()
