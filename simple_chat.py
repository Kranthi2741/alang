#!/usr/bin/env python3
"""
Simple command-line version of Alang that works in any terminal
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from alang.config import Config
from alang.gemini_client import GeminiClient


def main():
    print("🤖 Alang - AI Coding Assistant")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'help' for available commands")
    print("=" * 50)
    
    try:
        # Load configuration
        config = Config.load()
        config.validate()
        
        # Initialize Gemini client
        client = GeminiClient(config.gemini_api_key, config.model)
        
        print(f"\n✅ Connected to Gemini using model: {config.model}")
        print("💬 Start chatting with your AI assistant!\n")
        
        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Happy coding!")
                    break
                
                if user_input.lower() == 'help':
                    print("\n📚 Available commands:")
                    print("  help  - Show this help message")
                    print("  quit  - Exit the application")
                    print("  clear - Clear conversation history")
                    print("  Any other text will be sent to the AI assistant\n")
                    continue
                
                if user_input.lower() == 'clear':
                    client.clear_history()
                    print("🧹 Conversation history cleared!\n")
                    continue
                
                if not user_input:
                    continue
                
                # Get AI response
                print("🤖 Alang: ", end="", flush=True)
                response = client.generate_response(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Happy coding!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'quit' to exit.\n")
        
    except Exception as e:
        print(f"❌ Failed to start Alang: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
