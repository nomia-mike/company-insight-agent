#!/usr/bin/env python3
"""
Simple Chat with History Persistence
A minimal example showing how to preserve chat history between sessions.
"""

import os
import json
from datetime import datetime

import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Initialize OpenAI client
client = OpenAI()

# History file
HISTORY_FILE = "chat_history.json"

def save_history(history):
    """Save chat history to JSON file"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'history': history
            }, f, indent=2)
        print(f"✓ History saved to {HISTORY_FILE}")
    except Exception as e:
        print(f"✗ Error saving history: {e}")

def load_history():
    """Load chat history from JSON file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✓ Loaded history from {HISTORY_FILE}")
                return data.get('history', [])
        else:
            print("ℹ No existing history found")
            return []
    except Exception as e:
        print(f"✗ Error loading history: {e}")
        return []

def chat_function(message, history):
    """
    Main chat function that preserves history
    """
    # Clean history (remove any extra fields)
    clean_history = [{"role": h["role"], "content": h["content"]} for h in history]
    
    # Create messages list with history
    messages = clean_history + [{"role": "user", "content": message}]
    
    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    assistant_response = response.choices[0].message.content
    
    # Save updated history
    updated_history = clean_history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": assistant_response}
    ]
    save_history(updated_history)
    
    return assistant_response

def main():
    """Main function"""
    print("Starting Chat with History Persistence...")
    
    # Load existing history
    existing_history = load_history()
    print(f"Loaded {len(existing_history)} previous messages")
    
    # Create and launch chat interface
    chat_interface = gr.ChatInterface(
        fn=chat_function,
        title="Chat with History",
        description="Your conversations will be saved automatically!",
        examples=[
            "What is the capital of France?",
            "Tell me a joke",
            "What's 2+2?"
        ],
        type="messages"
    )
    
    chat_interface.launch()

if __name__ == "__main__":
    main() 