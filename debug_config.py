#!/usr/bin/env python3
"""
Debug script to check config loading
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from alang.config import Config

def main():
    print("🔍 Debugging Config Loading")
    print("=" * 30)
    
    try:
        config = Config.load()
        print(f"✅ Config loaded successfully")
        print(f"   API Key: '{config.gemini_api_key}'")
        print(f"   Model: '{config.model}'")
        print(f"   Data Dir: '{config.data_directory}'")
        print(f"   Debug: {config.debug}")
        
        try:
            config.validate()
            print("✅ Config validation passed")
        except Exception as e:
            print(f"❌ Config validation failed: {e}")
            
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
