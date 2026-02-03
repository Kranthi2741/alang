#!/bin/bash

# Alang Download and Install Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                 🤖 Alang Quick Installer                   ║"
    echo "║            AI Coding Assistant - One Click Install          ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if curl is available
check_curl() {
    if ! command -v curl &> /dev/null; then
        print_error "curl is not installed. Please install curl first."
        exit 1
    fi
}

# Download Alang
download_alang() {
    print_status "Downloading Alang..."
    
    # Create installation directory
    INSTALL_DIR="$HOME/alang"
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    # Download the files (replace with your actual GitHub repo URL)
    REPO_URL="https://github.com/yourusername/alang/archive/main.tar.gz"
    
    if curl -L -o alang.tar.gz "$REPO_URL"; then
        print_status "Download completed successfully"
        
        # Extract
        tar -xzf alang.tar.gz
        mv alang-main/* .
        rm -rf alang-main alang.tar.gz
        
        print_status "Files extracted successfully"
    else
        print_error "Failed to download Alang"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        print_error "Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    # Use python3 if available, otherwise python
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    else
        PYTHON_CMD="python"
        PIP_CMD="pip"
    fi
    
    # Install dependencies
    if $PIP_CMD install textual google-generativeai python-dotenv rich; then
        print_status "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi
}

# Setup configuration
setup_config() {
    print_status "Setting up configuration..."
    
    CONFIG_DIR="$HOME/.alang"
    CONFIG_FILE="$CONFIG_DIR/config.json"
    
    # Create config directory
    mkdir -p "$CONFIG_DIR"
    
    # Create default config
    cat > "$CONFIG_FILE" << EOF
{
  "gemini_api_key": "",
  "model": "models/gemini-2.5-flash",
  "data_directory": "~/.alang",
  "debug": false
}
EOF
    
    print_status "Configuration created at $CONFIG_FILE"
    print_warning "Please add your Gemini API key to the configuration file"
    print_warning "Get your API key from: https://makersuite.google.com/app/apikey"
}

# Create launcher script
create_launcher() {
    print_status "Creating launcher script..."
    
    LAUNCHER="/usr/local/bin/alang"
    
    # Check if we can write to /usr/local/bin
    if [ -w "/usr/local/bin" ]; then
        cat > "$LAUNCHER" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
$PYTHON_CMD simple_chat.py
EOF
        chmod +x "$LAUNCHER"
        print_status "Launcher created at $LAUNCHER"
    else
        print_warning "Cannot create system-wide launcher. You can run Alang with:"
        print_warning "cd $INSTALL_DIR && $PYTHON_CMD simple_chat.py"
    fi
}

# Create desktop shortcut (Linux)
create_desktop_shortcut() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_status "Creating desktop shortcut..."
        
        DESKTOP_DIR="$HOME/Desktop"
        mkdir -p "$DESKTOP_DIR"
        
        cat > "$DESKTOP_DIR/Alang.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Alang
Comment=AI Coding Assistant
Exec=$PYTHON_CMD $INSTALL_DIR/simple_chat.py
Icon=terminal
Terminal=true
Categories=Development;
EOF
        
        chmod +x "$DESKTOP_DIR/Alang.desktop"
        print_status "Desktop shortcut created"
    fi
}

# Main installation
main() {
    print_header
    print_status "Starting Alang installation..."
    
    check_curl
    download_alang
    install_dependencies
    setup_config
    create_launcher
    create_desktop_shortcut
    
    echo
    print_status "🎉 Alang has been installed successfully!"
    echo
    echo "📋 Next steps:"
    echo "1. Add your Gemini API key to: $CONFIG_FILE"
    echo "2. Run 'alang' from terminal or use the desktop shortcut"
    echo "3. For help, visit: https://github.com/yourusername/alang"
    echo
    print_status "Happy coding! 🚀"
}

# Run installation
main "$@"
