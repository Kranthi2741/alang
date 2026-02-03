#!/usr/bin/env python3
"""
Alang Installer - One-click installation script
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_colored(text, color="white"):
    """Print colored text"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m", 
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def check_python():
    """Check if Python is installed"""
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print_colored("❌ Python 3.8 or higher is required", "red")
            print_colored(f"   Found: Python {version.major}.{version.minor}.{version.micro}", "red")
            return False
        print_colored(f"✅ Python {version.major}.{version.minor}.{version.micro} detected", "green")
        return True
    except:
        print_colored("❌ Python not found", "red")
        return False

def install_dependencies():
    """Install required packages"""
    print_colored("📦 Installing dependencies...", "blue")
    
    packages = [
        "textual>=0.47.0",
        "google-generativeai>=0.4.0", 
        "python-dotenv>=1.0.0",
        "rich>=13.0.0"
    ]
    
    for package in packages:
        try:
            print_colored(f"   Installing {package}...", "yellow")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_colored(f"   ✅ {package} installed", "green")
        except subprocess.CalledProcessError:
            print_colored(f"   ❌ Failed to install {package}", "red")
            return False
    
    return True

def create_config():
    """Create configuration directory and file"""
    config_dir = Path.home() / ".alang"
    config_file = config_dir / "config.json"
    
    print_colored("⚙️ Setting up configuration...", "blue")
    
    # Create directory
    config_dir.mkdir(exist_ok=True)
    
    # Create default config if it doesn't exist
    if not config_file.exists():
        default_config = {
            "gemini_api_key": "",
            "model": "models/gemini-2.5-flash",
            "data_directory": "~/.alang",
            "debug": False
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print_colored(f"   📄 Created config file: {config_file}", "green")
        print_colored("   ⚠️  Please add your Gemini API key to the config file", "yellow")
        print_colored("   📌 Get your API key from: https://makersuite.google.com/app/apikey", "cyan")
    else:
        print_colored(f"   ✅ Config file already exists: {config_file}", "green")
    
    return config_file

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if sys.platform != "win32":
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Alang.lnk")
        target = sys.executable
        wDir = os.path.dirname(os.path.abspath(__file__))
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.Arguments = f'"{os.path.join(wDir, "simple_chat.py")}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print_colored(f"   🖥️  Desktop shortcut created: {path}", "green")
        
    except ImportError:
        print_colored("   ⚠️  Could not create desktop shortcut (winshell not available)", "yellow")
    except Exception as e:
        print_colored(f"   ⚠️  Could not create desktop shortcut: {e}", "yellow")

def main():
    """Main installation function"""
    print_colored("╔══════════════════════════════════════════════════════════════╗", "cyan")
    print_colored("║                    🤖 Alang Installer                        ║", "cyan")
    print_colored("║              AI Coding Assistant Installer                  ║", "cyan")
    print_colored("╚══════════════════════════════════════════════════════════════╝", "cyan")
    print()
    
    # Check Python
    if not check_python():
        print_colored("❌ Installation failed: Python requirement not met", "red")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print_colored("❌ Installation failed: Could not install dependencies", "red")
        return False
    
    # Create configuration
    config_file = create_config()
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print()
    print_colored("🎉 Installation completed successfully!", "green")
    print()
    print_colored("📋 Next steps:", "blue")
    print_colored("1. Add your Gemini API key to:", "white")
    print_colored(f"   {config_file}", "cyan")
    print_colored("2. Run Alang with:", "white")
    print_colored("   python simple_chat.py", "cyan")
    print_colored("3. Or double-click the desktop shortcut (if created)", "white")
    print()
    print_colored("🚀 Happy coding with Alang!", "green")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n❌ Installation cancelled", "red")
    except Exception as e:
        print_colored(f"\n❌ Installation failed: {e}", "red")
