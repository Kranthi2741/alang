@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Alang Download and Install Script for Windows

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                 🤖 Alang Quick Installer                   ║
echo ║            AI Coding Assistant - One Click Install          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [INFO] Starting Alang installation...
echo.

:: Check if curl is available
where curl >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] curl is not available. Please install curl or use Git Bash.
    echo You can download curl from: https://curl.se/windows/
    pause
    exit /b 1
)

echo [INFO] curl found, proceeding with installation...
echo.

:: Set installation directory
set "INSTALL_DIR=%USERPROFILE%\alang"
echo [INFO] Installation directory: %INSTALL_DIR%

:: Create installation directory
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

:: Download Alang (you'll need to replace this with your actual download URL)
echo [INFO] Downloading Alang...
cd /d "%INSTALL_DIR%"

:: For now, copy from current directory (replace with actual download)
echo [INFO] Copying files from current location...
xcopy /E /I /Y "d:\lancer\opencode_ai\alang-python\*" "%INSTALL_DIR%\" >nul

if %errorlevel% neq 0 (
    echo [ERROR] Failed to copy files
    pause
    exit /b 1
)

echo [INFO] Files copied successfully
echo.

:: Install Python dependencies
echo [INFO] Installing Python dependencies...

python -m pip install textual google-generativeai python-dotenv rich --quiet

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [INFO] Dependencies installed successfully
echo.

:: Setup configuration
echo [INFO] Setting up configuration...

set "CONFIG_DIR=%USERPROFILE%\.alang"
set "CONFIG_FILE=%CONFIG_DIR%\config.json"

if not exist "%CONFIG_DIR%" (
    mkdir "%CONFIG_DIR%"
)

:: Create config file
(
echo {
echo   "gemini_api_key": "",
echo   "model": "models/gemini-2.5-flash",
echo   "data_directory": "~/.alang",
echo   "debug": false
echo }
) > "%CONFIG_FILE%"

echo [INFO] Configuration created at %CONFIG_FILE%
echo [WARN] Please add your Gemini API key to the configuration file
echo [WARN] Get your API key from: https://makersuite.google.com/app/apikey
echo.

:: Create desktop shortcut
echo [INFO] Creating desktop shortcut...

set "SHORTCUT=%USERPROFILE%\Desktop\Alang.lnk"

:: Create a temporary VBScript to create the shortcut
set "VBSCRIPT=%TEMP%\CreateShortcut.vbs"

(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%SHORTCUT%"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "python"
echo oLink.Arguments = "%INSTALL_DIR%\simple_chat.py"
echo oLink.WorkingDirectory = "%INSTALL_DIR%"
echo oLink.Description = "Alang AI Coding Assistant"
echo oLink.Save
) > "%VBSCRIPT%"

cscript //nologo "%VBSCRIPT%"
del "%VBSCRIPT%"

echo [INFO] Desktop shortcut created
echo.

:: Create launcher script
echo [INFO] Creating launcher script...

(
echo @echo off
echo cd /d "%INSTALL_DIR%"
echo python simple_chat.py
echo pause
) > "%INSTALL_DIR%\run_alang.bat"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 Installation Complete!                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📋 Next steps:
echo 1. Add your Gemini API key to: %CONFIG_FILE%
echo 2. Double-click the desktop shortcut "Alang"
echo 3. Or run: %INSTALL_DIR%\run_alang.bat
echo.
echo 🚀 Happy coding with Alang!
echo.
pause
