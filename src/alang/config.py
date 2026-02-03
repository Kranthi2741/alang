"""
Configuration management for Alang
"""

import json
import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration class for Alang"""
    
    def __init__(self):
        self.gemini_api_key: str = ""
        self.model: str = "gemini-1.5-pro"
        self.data_directory: str = "~/.alang"
        self.debug: bool = False
        
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """Load configuration from file or environment"""
        config = cls()
        
        # Determine config file path
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = Path.home() / ".alang" / "config.json"
        
        # Load from file if it exists
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    
                config.gemini_api_key = data.get("gemini_api_key", "")
                config.model = data.get("model", "gemini-1.5-pro")
                config.data_directory = data.get("data_directory", "~/.alang")
                config.debug = data.get("debug", False)
                
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load config file {config_file}: {e}")
        
        # Override with environment variables
        if os.getenv("GEMINI_API_KEY"):
            config.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if os.getenv("ALANG_MODEL"):
            config.model = os.getenv("ALANG_MODEL")
            
        if os.getenv("ALANG_DATA_DIR"):
            config.data_directory = os.getenv("ALANG_DATA_DIR")
            
        if os.getenv("ALANG_DEBUG"):
            config.debug = os.getenv("ALANG_DEBUG").lower() in ("true", "1", "yes")
        
        return config
    
    def validate(self) -> None:
        """Validate configuration"""
        if not self.gemini_api_key:
            raise ValueError(
                "Gemini API key is required. Set it in config file or GEMINI_API_KEY environment variable. "
                "Get your API key from: https://makersuite.google.com/app/apikey"
            )
    
    def ensure_data_directory(self) -> Path:
        """Ensure data directory exists and return Path object"""
        # Expand ~ to home directory
        if self.data_directory.startswith("~"):
            data_dir = Path.home() / self.data_directory[2:]
        else:
            data_dir = Path(self.data_directory)
        
        # Create directory if it doesn't exist
        data_dir.mkdir(parents=True, exist_ok=True)
        
        return data_dir
    
    def save(self, config_path: Optional[str] = None) -> None:
        """Save configuration to file"""
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = Path.home() / ".alang" / "config.json"
        
        # Create directory if it doesn't exist
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "gemini_api_key": self.gemini_api_key,
            "model": self.model,
            "data_directory": self.data_directory,
            "debug": self.debug
        }
        
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            "gemini_api_key": self.gemini_api_key,
            "model": self.model,
            "data_directory": self.data_directory,
            "debug": self.debug
        }
