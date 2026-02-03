"""
Gemini API client for Alang
"""

import google.genai as genai
from typing import List, Dict, Optional
import logging


class GeminiClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self, api_key: str, model: str = "models/gemini-2.5-flash"):
        """Initialize Gemini client
        
        Args:
            api_key: Google Gemini API key
            model: Model name to use
        """
        self.api_key = api_key
        self.model_name = model
        
        # Configure the API
        self.client = genai.Client(api_key=api_key)
        
        # Initialize the model
        self.model = model
        
        # Configure generation parameters
        self.config = {
            "temperature": 0.1,  # Lower temperature for more consistent responses
            "top_k": 40,
            "top_p": 0.95,
            "max_output_tokens": 8192,
        }
        
        self.logger = logging.getLogger(__name__)
    
    def generate_response(self, message: str, history: Optional[List[Dict]] = None) -> str:
        """Generate a response from Gemini
        
        Args:
            message: User message
            history: Optional conversation history
            
        Returns:
            Generated response text
        """
        try:
            # Create contents list
            contents = []
            
            # Add history if provided
            if history:
                for msg in history:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })
            
            # Add current message
            contents.append({
                "role": "user",
                "parts": [{"text": message}]
            })
            
            # Generate response using the new API
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=self.config
            )
            
            if response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return f"Error: {str(e)}"
    
    def get_conversation_history(self) -> List[Dict]:
        """Get current conversation history
        
        Returns:
            List of message dictionaries
        """
        # For the new API, we'll need to track history differently
        # For now, return empty list - this will be implemented when we add history tracking
        return []
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        # For the new API, this will be implemented when we add history tracking
        pass
    
    def get_model_info(self) -> Dict:
        """Get information about the current model
        
        Returns:
            Dictionary with model information
        """
        return {
            "name": self.model_name,
            "api_key": "***" + self.api_key[-4:] if self.api_key else None,
            "history_length": 0  # Will be updated when we implement history tracking
        }
