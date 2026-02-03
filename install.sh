#!/bin/bash

# Alang Installation Script for Python
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🤖 Alang Installer                        ║"
    echo "║              AI Coding Assistant Installer                  ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        if ! command -v python &> /dev/null; then
            print_error "Python is not installed. Please install Python 3.8 or higher."
            echo "Visit: https://www.python.org/downloads/"
            exit 1
        else
            PYTHON_CMD="python"
        fi
    else
        PYTHON_CMD="python3"
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_status "Found Python version: $PYTHON_VERSION"
    
    # Check if version is 3.8 or higher
    if $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        print_status "Python version is compatible"
    else
        print_error "Python 3.8 or higher is required"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        print_error "pip is not installed. Please install pip."
        echo "Visit: https://pip.pypa.io/en/stable/installation/"
        exit 1
    fi
    
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    else
        PIP_CMD="pip"
    fi
    
    print_status "Using pip: $PIP_CMD"
}

# Install Alang
install_alang() {
    print_status "Installing Alang..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # Clone the repository
    print_status "Downloading Alang..."
    if command -v git &> /dev/null; then
        git clone https://github.com/yourusername/alang.git .
    else
        print_error "Git is required to install Alang"
        exit 1
    fi
    
    # Install the package
    print_status "Installing Python package..."
    $PIP_CMD install -e .
    
    # Cleanup
    cd /
    rm -rf "$TEMP_DIR"
    
    print_status "Installation completed successfully!"
}

# Setup configuration
setup_config() {
    print_status "Setting up configuration..."
    
    CONFIG_DIR="$HOME/.alang"
    CONFIG_FILE="$CONFIG_DIR/config.json"
    
    # Create config directory
    mkdir -p "$CONFIG_DIR"
    
    # Create default config if it doesn't exist
    if [ ! -f "$CONFIG_FILE" ]; then
        cat > "$CONFIG_FILE" << EOF
{
  "gemini_api_key": "",
  "model": "gemini-1.5-pro",
  "data_directory": "~/.alang",
  "debug": false
}
EOF
        print_status "Created configuration file at $CONFIG_FILE"
        print_warning "Please add your Gemini API key to the configuration file"
        print_warning "You can get your API key from: https://makersuite.google.com/app/apikey"
    else
        print_status "Configuration file already exists at $CONFIG_FILE"
    fi
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    if command -v alang &> /dev/null; then
        print_status "✅ Alang command is available"
        
        # Test if it can import
        if $PYTHON_CMD -c "import alang" 2>/dev/null; then
            print_status "✅ Python package is correctly installed"
        else
            print_warning "⚠️  Python package import failed"
        fi
    else
        print_error "❌ Alang command is not available"
        return 1
    fi
}

# Main installation flow
main() {
    print_header
    print_status "Starting Alang installation..."
    
    check_python
    check_pip
    install_alang
    setup_config
    verify_installation
    
    echo
    print_status "🎉 Alang has been installed successfully!"
    echo
    echo "Next steps:"
    echo "1. Add your Gemini API key to ~/.alang/config.json"
    echo "2. Run 'alang' to start your AI coding assistant"
    echo "3. For help, run 'alang --help'"
    echo
    echo "Documentation: https://github.com/yourusername/alang"
    echo
    print_status "Happy coding! 🚀"
}

# Run main function
main "$@"
