"""
a
by m
"""
import os

import gradio as gr
from dotenv import load_dotenv

load_dotenv(override=True)


from openai import OpenAI
client = OpenAI()

response = client.responses.create(
  model="gpt-5",
  input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)

