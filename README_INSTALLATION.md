# 🚀 Alang Installation Guide

## Quick Installation Options

### Option 1: One-Click Installation (Recommended)

#### Windows Users:
```cmd
curl -fsSL https://raw.githubusercontent.com/yourusername/alang/main/download_and_install.bat -o install.bat && install.bat
```

Or download and run `download_and_install.bat`

#### Linux/Mac Users:
```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/alang/main/download_and_install.sh | bash
```

### Option 2: Manual Installation

#### Step 1: Download Alang
```bash
# Clone the repository
git clone https://github.com/yourusername/alang.git
cd alang

# Or download the ZIP file
# https://github.com/yourusername/alang/archive/main.zip
```

#### Step 2: Install Dependencies
```bash
pip install textual google-generativeai python-dotenv rich
```

#### Step 3: Configure
```bash
# Create config directory
mkdir -p ~/.alang

# Create config file
cat > ~/.alang/config.json << EOF
{
  "gemini_api_key": "your-api-key-here",
  "model": "models/gemini-2.5-flash",
  "data_directory": "~/.alang",
  "debug": false
}
EOF
```

#### Step 4: Run Alang
```bash
# Simple version (works in any terminal)
python simple_chat.py

# TUI version (rich interface)
python main.py
```

## 📋 Requirements

- **Python 3.8+** - Download from [python.org](https://python.org)
- **Gemini API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Internet Connection** - For API calls

## 🎯 What You Get

✅ **AI Coding Assistant** powered by Google Gemini  
✅ **Beautiful TUI Interface** with rich formatting  
✅ **Simple Chat Mode** for any terminal  
✅ **Session Management** with SQLite storage  
✅ **File Operations** and coding tools  
✅ **Cross-Platform** (Windows, Mac, Linux)  

## 🔧 Configuration

Edit `~/.alang/config.json`:

```json
{
  "gemini_api_key": "AIzaSy...your-key-here",
  "model": "models/gemini-2.5-flash",
  "data_directory": "~/.alang",
  "debug": false
}
```

## 🖥️ Running Alang

### Simple Chat Mode (Recommended for VS Code):
```bash
python simple_chat.py
```

### Rich TUI Mode:
```bash
python main.py
```

### Desktop Shortcut:
- Windows: Double-click "Alang" on desktop
- Linux: Double-click "Alang.desktop"

## 🎮 Keyboard Shortcuts

- `Ctrl+C` - Quit application
- `Ctrl+S` - Send message
- `Ctrl+L` - Clear chat
- `Enter` - Send message
- `Shift+Enter` - New line

## 🆘 Troubleshooting

### Blank Screen in TUI Mode?
Use the simple chat mode: `python simple_chat.py`

### API Key Issues?
1. Get key from: https://makersuite.google.com/app/apikey
2. Add to: `~/.alang/config.json`
3. Restart Alang

### Python Not Found?
Install Python 3.8+ from: https://python.org

## 📱 Mobile/Remote Access

Want to use Alang on your phone or other devices?

1. **Install on a server/VPS**
2. **Use SSH**: `ssh user@server -t "cd ~/alang && python simple_chat.py"`
3. **Web version coming soon!**

## 🔄 Updates

To update Alang:
```bash
cd alang
git pull origin main
pip install -r requirements.txt --upgrade
```

## 🤝 Contributing

Contributions welcome! 
- Fork the repository
- Create a feature branch
- Submit a Pull Request

## 📞 Support

- 📧 Email: your.email@example.com
- 🐛 Issues: https://github.com/yourusername/alang/issues
- 📖 Docs: https://github.com/yourusername/alang/wiki

---

**Made with ❤️ by developers, for developers**
