#!/usr/bin/env python3
"""
Alang - Your AI Coding Assistant
A terminal-based AI assistant powered by Google Gemini
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from alang.app import AlangApp
from alang.config import Config


def main():
    parser = argparse.ArgumentParser(
        description="Alang - Your AI Coding Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  alang                           # Start interactive mode
  alang --debug                   # Start with debug logging
  alang --config custom.json     # Use custom config file
        """
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to configuration file (default: ~/.alang/config.json)"
    )
    
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = Config.load(args.config)
        config.debug = args.debug
        
        # Validate configuration
        config.validate()
        
        # Create and run the app
        app = AlangApp(config)
        app.run()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
