# Alang - Your AI Coding Assistant

<p align="center">
    <h2>🤖 Alang</h2>
    <p>Your intelligent coding companion powered by Google Gemini</p>
</p>

Alang is a powerful terminal-based AI assistant that helps developers with coding tasks, debugging, and learning - right in your terminal.

## Features

- 🧠 **AI-Powered**: Integrated with Google Gemini for intelligent coding assistance
- 💬 **Interactive Chat**: Natural language conversation with your AI assistant
- 🛠️ **Code Tools**: File operations, search, grep, and code analysis
- 📝 **Session Management**: Save and resume your coding sessions
- 🎨 **Beautiful TUI**: Modern terminal interface built with Textual
- 🔧 **Easy Setup**: Simple configuration with your Gemini API key
- 🗄️ **Local Storage**: SQLite database for sessions and message history
- 🚀 **Cross-Platform**: Works on Windows, macOS, and Linux

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Installation

#### Option 1: Install from PyPI (recommended)
```bash
pip install alang
```

#### Option 2: Install from source
```bash
git clone https://github.com/yourusername/alang.git
cd alang
pip install -e .
```

### Configuration

Create a configuration file at `~/.alang/config.json`:

```json
{
  "gemini_api_key": "your-gemini-api-key-here",
  "model": "gemini-1.5-pro",
  "data_directory": "~/.alang",
  "debug": false
}
```

Or set the API key as environment variable:

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

### Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and add it to your configuration

## Usage

```bash
# Start interactive mode
alang

# Get help
alang --help

# Run with custom config
alang --config /path/to/config.json

# Enable debug mode
alang --debug
```

## Available Tools

Alang provides various tools to help with your coding:

- **📄 File Operations**: Read, write, edit files
- **🔍 Search**: Find files and search within files
- **💻 Code Analysis**: Understand and explain code
- **🖥️ Terminal**: Execute shell commands
- **📊 Statistics**: View session and usage statistics

## Keyboard Shortcuts

- `Ctrl+C`: Quit application
- `Ctrl+K`: Command palette (coming soon)
- `Ctrl+S`: Send message
- `Ctrl+L`: Clear chat
- `Escape`: Focus input field
- `Enter`: Send message
- `Shift+Enter`: New line in input

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `gemini_api_key` | string | - | Your Google Gemini API key |
| `model` | string | `gemini-1.5-pro` | Gemini model to use |
| `data_directory` | string | `~/.alang` | Directory for storing data |
| `debug` | boolean | `false` | Enable debug logging |

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/alang.git
cd alang

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/

# Lint code
flake8 src/
```

### Project Structure

```
alang/
├── src/alang/
│   ├── __init__.py          # Package initialization
│   ├── app.py               # Main application
│   ├── config.py            # Configuration management
│   ├── gemini_client.py     # Gemini API client
│   ├── database.py          # SQLite database
│   ├── tools.py             # Tool system
│   └── widgets.py           # TUI widgets
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── setup.py                 # Package setup
└── README.md               # Documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## License

MIT License - see LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

## Roadmap

- [ ] Plugin system for custom tools
- [ ] Multiple AI provider support
- [ ] Web interface
- [ ] Team collaboration features
- [ ] Code completion integration
- [ ] Git integration

## Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual) for the TUI
- Powered by [Google Gemini](https://ai.google.dev/)
- Inspired by [Crush](https://github.com/charmbracelet/crush) and other AI coding assistants

---

**Made with ❤️ by developers, for developers**
