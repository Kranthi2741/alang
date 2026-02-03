"""
Custom widgets for Alang TUI
"""

from textual.containers import Vertical, Horizontal
from textual.widgets import TextArea, Input, Static
from textual.reactive import reactive
from textual.message import Message
from rich.markdown import Markdown
from rich.text import Text
import asyncio


class MessageSubmitted(Message):
    """Message sent when user submits input"""
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message


class MessageDisplay(Static):
    """Display a single message"""
    
    def __init__(self, role: str, content: str, **kwargs):
        super().__init__(**kwargs)
        self.role = role
        self.content = content
        self._update_display()
    
    def _update_display(self):
        """Update the display based on role and content"""
        if self.role == "user":
            self.styles.background = "$surface"
            self.styles.margin = (1, 0)
            self.styles.padding = (1, 1)
            
            # Simple text display for user messages
            self.update(f"👤 **You:**\n{self.content}")
            
        elif self.role == "assistant":
            self.styles.background = "$primary"
            self.styles.margin = (1, 0)
            self.styles.padding = (1, 1)
            
            # Render markdown for assistant messages
            try:
                markdown = Markdown(self.content)
                self.update(markdown)
            except:
                self.update(f"🤖 **Alang:**\n{self.content}")
                
        elif self.role == "system":
            self.styles.background = "$error"
            self.styles.margin = (1, 0)
            self.styles.padding = (1, 1)
            self.update(f"🔧 **System:**\n{self.content}")


class ChatContainer(Vertical):
    """Container for chat messages"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
        self.thinking = reactive(False)
    
    def compose(self):
        """Compose the chat container"""
        yield Vertical(id="messages-container")
    
    def add_message(self, role: str, content: str):
        """Add a new message to the chat"""
        message_display = MessageDisplay(role, content)
        self.messages.append(message_display)
        
        # Add to container
        container = self.query_one("#messages-container", Vertical)
        container.mount(message_display)
        
        # Scroll to bottom
        self.scroll_end(animate=True)
    
    def clear_messages(self):
        """Clear all messages"""
        container = self.query_one("#messages-container", Vertical)
        container.remove_children()
        self.messages = []
    
    def set_thinking(self, is_thinking: bool):
        """Set thinking state"""
        self.thinking = is_thinking
        
        if is_thinking:
            # Add thinking indicator
            thinking_msg = MessageDisplay("system", "🤔 *Thinking...*")
            container = self.query_one("#messages-container", Vertical)
            container.mount(thinking_msg)
            self.scroll_end(animate=True)
        else:
            # Remove thinking indicator
            container = self.query_one("#messages-container", Vertical)
            children = container.children
            if children and "Thinking..." in str(children[-1]):
                children[-1].remove()
    
    def watch_thinking(self, is_thinking: bool):
        """Watch for thinking state changes"""
        self.set_thinking(is_thinking)


class InputArea(TextArea):
    """Input area for user messages"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = "markdown"  # Enable markdown syntax highlighting
        self.show_line_numbers = False
        self.soft_wrap = True
    
    def compose(self):
        """Compose the input area"""
        yield self
    
    def get_text(self) -> str:
        """Get the current text"""
        return self.text
    
    def clear(self):
        """Clear the input"""
        self.text = ""
        self.cursor_position = (0, 0)
    
    def on_key(self, event):
        """Handle key events"""
        if event.key == "enter":
            # Check if shift+enter (new line) or just enter (send)
            if not event.is_shift:
                # Send message
                message = self.get_text().strip()
                if message:
                    self.post_message(MessageSubmitted(message))
                event.prevent_default()
            else:
                # Allow new line with shift+enter
                return
        elif event.key == "ctrl+s":
            # Send message with Ctrl+S
            message = self.get_text().strip()
            if message:
                self.post_message(MessageSubmitted(message))
            event.prevent_default()
