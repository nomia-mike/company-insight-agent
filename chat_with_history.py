#!/usr/bin/env python3
"""
Chat Interface with History Persistence
A standalone Python script that provides a chat interface with automatic history saving.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any

import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

class ChatHistoryManager:
    """Manages chat history persistence"""
    
    def __init__(self, history_file: str = "chat_history.json"):
        self.history_file = history_file
    
    def save_chat_history(self, history: List[Dict[str, str]]) -> None:
        """Save chat history to a JSON file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'history': history
                }, f, indent=2, ensure_ascii=False)
            print(f"Chat history saved to {self.history_file}")
        except Exception as e:
            print(f"Error saving chat history: {e}")
    
    def load_chat_history(self) -> List[Dict[str, str]]:
        """Load chat history from JSON file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"Loaded chat history from {self.history_file}")
                    return data.get('history', [])
            else:
                print("No existing chat history found")
                return []
        except Exception as e:
            print(f"Error loading chat history: {e}")
            return []
    
    def clear_chat_history(self) -> None:
        """Clear the chat history file"""
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
                print(f"Chat history cleared")
            else:
                print("No chat history file to clear")
        except Exception as e:
            print(f"Error clearing chat history: {e}")
    
    def get_history_info(self) -> Dict[str, Any]:
        """Get information about the chat history"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history = data.get('history', [])
                    return {
                        'exists': True,
                        'message_count': len(history),
                        'last_updated': data.get('timestamp', 'Unknown'),
                        'file_size': os.path.getsize(self.history_file)
                    }
            else:
                return {
                    'exists': False,
                    'message_count': 0,
                    'last_updated': None,
                    'file_size': 0
                }
        except Exception as e:
            print(f"Error getting history info: {e}")
            return {
                'exists': False,
                'message_count': 0,
                'last_updated': None,
                'file_size': 0
            }

class ChatInterface:
    """Main chat interface with history persistence"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model
        self.history_manager = ChatHistoryManager()
        
        # Load existing history
        self.existing_history = self.history_manager.load_chat_history()
        print(f"Loaded {len(self.existing_history)} previous messages")
    
    def chat_function(self, message: str, history: List[Dict[str, str]]) -> str:
        """
        Main chat function that handles messages and saves history
        """
        # Clean up history to ensure it only contains role and content
        clean_history = [{"role": h["role"], "content": h["content"]} for h in history]
        
        # Create the full message list including history
        messages = clean_history + [{"role": "user", "content": message}]
        
        # Get response from OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        assistant_response = response.choices[0].message.content
        
        # Save the updated history (including the new exchange)
        updated_history = clean_history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": assistant_response}
        ]
        self.history_manager.save_chat_history(updated_history)
        
        return assistant_response
    
    def clear_history(self) -> str:
        """Clear chat history and return confirmation message"""
        self.history_manager.clear_chat_history()
        return "Chat history has been cleared."
    
    def get_history_info(self) -> str:
        """Get information about the current chat history"""
        info = self.history_manager.get_history_info()
        if info['exists']:
            return f"Chat History Info:\n- Messages: {info['message_count']}\n- Last Updated: {info['last_updated']}\n- File Size: {info['file_size']} bytes"
        else:
            return "No chat history found."
    
    def launch(self, share: bool = False, server_name: str = "127.0.0.1", server_port: int = 7860):
        """Launch the chat interface"""
        
        # Create the main chat interface
        with gr.Blocks(title="Chat with History Persistence") as demo:
            gr.Markdown("# Chat Interface with History Persistence")
            gr.Markdown("Your conversations will be automatically saved and restored between sessions.")
            
            with gr.Row():
                with gr.Column(scale=3):
                    # Main chat interface
                    chat_interface = gr.ChatInterface(
                        fn=self.chat_function,
                        title="Chat",
                        description="Start a conversation...",
                        examples=[
                            "What is the capital of France?",
                            "Tell me a joke",
                            "What's the weather like?",
                            "Explain quantum computing in simple terms"
                        ],
                        retry_btn=None,
                        undo_btn=None,
                        clear_btn="Clear Chat",
                        type="messages"
                    )
                
                with gr.Column(scale=1):
                    # History management panel
                    gr.Markdown("### History Management")
                    
                    info_btn = gr.Button("Show History Info", variant="secondary")
                    info_output = gr.Textbox(label="History Information", interactive=False)
                    
                    clear_btn = gr.Button("Clear History", variant="stop")
                    clear_output = gr.Textbox(label="Status", interactive=False)
                    
                    # Connect buttons
                    info_btn.click(
                        fn=self.get_history_info,
                        outputs=info_output
                    )
                    
                    clear_btn.click(
                        fn=self.clear_history,
                        outputs=clear_output
                    )
            
            # Show initial history info
            demo.load(
                fn=self.get_history_info,
                outputs=info_output
            )
        
        # Launch the interface
        demo.launch(
            share=share,
            server_name=server_name,
            server_port=server_port
        )

def main():
    """Main function to run the chat interface"""
    print("Starting Chat Interface with History Persistence...")
    print("Make sure you have set up your OpenAI API key in your .env file")
    
    # Create and launch the chat interface
    chat_interface = ChatInterface()
    chat_interface.launch()

if __name__ == "__main__":
    main() 