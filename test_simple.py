#!/usr/bin/env python3
"""
Simple test to check if basic imports work
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from alang.config import Config
    print("✅ Config import successful")
    
    config = Config.load()
    print(f"✅ Config loaded successfully")
    print(f"   API Key: {config.gemini_api_key[:20]}...")
    print(f"   Model: {config.model}")
    
    try:
        config.validate()
        print("✅ Config validation successful")
    except Exception as e:
        print(f"❌ Config validation failed: {e}")
    
    try:
        from alang.gemini_client import GeminiClient
        print("✅ GeminiClient import successful")
        
        client = GeminiClient(config.gemini_api_key, config.model)
        print("✅ GeminiClient initialized successfully")
        
        # Test a simple generation
        response = client.generate_response("Hello, say hi back!")
        print(f"✅ Gemini response: {response[:100]}...")
        
    except Exception as e:
        print(f"❌ GeminiClient failed: {e}")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Test completed!")
