"""
Main application class for Alang
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, TextArea, Static, LoadingIndicator
from textual.reactive import reactive
from textual.binding import Binding
from textual.message import Message
from rich.markdown import Markdown
import asyncio
import logging

from .config import Config
from .gemini_client import GeminiClient
from .database import Database
from .widgets import ChatContainer, InputArea


class AlangApp(App):
    """Main Alang application"""
    
    CSS = """
    Screen {
        layout: vertical;
    }
    
    #header {
        background: $primary;
        text-align: center;
        height: 3;
    }
    
    #main-container {
        height: 1fr;
    }
    
    #chat-container {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }
    
    #input-area {
        height: 10;
        border: solid $secondary;
        padding: 1;
    }
    
    .user-message {
        background: $surface;
        margin: 1 0;
        padding: 1;
    }
    
    .assistant-message {
        background: $primary;
        margin: 1 0;
        padding: 1;
    }
    
    .thinking {
        color: $warning;
        text-style: italic;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+k", "command_palette", "Commands"),
        Binding("ctrl+l", "clear_chat", "Clear"),
        Binding("ctrl+s", "send_message", "Send"),
        Binding("escape", "focus_input", "Focus Input"),
    ]
    
    TITLE = "🤖 Alang - AI Coding Assistant"
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.gemini_client = None
        self.database = None
        self.current_session_id = None
        self.is_thinking = reactive(False)
        
        # Setup logging
        if config.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        
        self.logger = logging.getLogger(__name__)
    
    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header(id="header")
        
        with Container(id="main-container"):
            yield ChatContainer(id="chat-container")
            yield InputArea(id="input-area")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the application when mounted"""
        self._initialize_services()
        self._load_welcome_message()
    
    def _initialize_services(self) -> None:
        """Initialize Gemini client and database"""
        try:
            # Initialize Gemini client
            self.gemini_client = GeminiClient(
                api_key=self.config.gemini_api_key,
                model=self.config.model
            )
            
            # Initialize database
            data_dir = self.config.ensure_data_directory()
            self.database = Database(data_dir / "alang.db")
            
            # Create or get current session
            self.current_session_id = self.database.create_session("Default Session")
            
            self.logger.info("Services initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize services: {e}")
            self._show_error(f"Failed to initialize: {e}")
    
    def _load_welcome_message(self) -> None:
        """Load welcome message"""
        welcome_text = """# 🤖 Welcome to Alang!

Your AI coding assistant is ready to help you with:

- **Code writing** and debugging
- **File operations** and management
- **Problem solving** and explanations
- **Learning** new programming concepts

Just type your message below and press Enter to get started!

---

**Keyboard Shortcuts:**
- `Ctrl+C` - Quit
- `Ctrl+K` - Command palette
- `Ctrl+L` - Clear chat
- `Ctrl+S` - Send message
- `Escape` - Focus input field"""
        
        chat_container = self.query_one("#chat-container", ChatContainer)
        chat_container.add_message("assistant", welcome_text)
    
    def _show_error(self, error_message: str) -> None:
        """Show error message to user"""
        chat_container = self.query_one("#chat-container", ChatContainer)
        chat_container.add_message("system", f"❌ Error: {error_message}")
    
    async def action_send_message(self) -> None:
        """Send the current message"""
        input_area = self.query_one("#input-area", InputArea)
        message = input_area.get_text()
        
        if not message.strip():
            return
        
        # Clear input
        input_area.clear()
        
        # Add user message to chat
        chat_container = self.query_one("#chat-container", ChatContainer)
        chat_container.add_message("user", message)
        
        # Save to database
        if self.database:
            self.database.save_message(self.current_session_id, "user", message)
        
        # Set thinking state
        self.is_thinking = True
        chat_container.set_thinking(True)
        
        try:
            # Generate response
            response = await asyncio.to_thread(
                self.gemini_client.generate_response, 
                message
            )
            
            # Add response to chat
            chat_container.add_message("assistant", response)
            
            # Save to database
            if self.database:
                self.database.save_message(self.current_session_id, "assistant", response)
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            chat_container.add_message("system", f"❌ Error: {str(e)}")
        
        finally:
            self.is_thinking = False
            chat_container.set_thinking(False)
    
    def action_clear_chat(self) -> None:
        """Clear the chat"""
        chat_container = self.query_one("#chat-container", ChatContainer)
        chat_container.clear_messages()
        
        # Clear Gemini client history
        if self.gemini_client:
            self.gemini_client.clear_history()
        
        # Create new session
        if self.database:
            self.current_session_id = self.database.create_session("New Session")
        
        self._load_welcome_message()
    
    def action_focus_input(self) -> None:
        """Focus the input area"""
        input_area = self.query_one("#input-area", InputArea)
        input_area.focus()
    
    def action_command_palette(self) -> None:
        """Show command palette (placeholder)"""
        self.notify("Command palette coming soon!")
    
    def on_input_area_submitted(self, message: str) -> None:
        """Handle message submission from input area"""
        asyncio.create_task(self.action_send_message())
