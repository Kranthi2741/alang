@echo off
echo 🤖 Alang Installation for Windows
echo ====================================

REM Create installation directory
set INSTALL_DIR=%USERPROFILE%\alang
echo 📁 Creating installation directory: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files from current directory
echo 📋 Copying Alang files...
xcopy /E /I /Y "*" "%INSTALL_DIR%\" >nul 2>&1

REM Install Python dependencies
echo 📦 Installing Python dependencies...
python -m pip install textual google-generativeai python-dotenv rich --quiet

REM Create configuration
set CONFIG_DIR=%USERPROFILE%\.alang
set CONFIG_FILE=%CONFIG_DIR%\config.json

echo ⚙️ Setting up configuration...
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"

echo { > "%CONFIG_FILE%"
echo   "gemini_api_key": "", >> "%CONFIG_FILE%"
echo   "model": "models/gemini-2.5-flash", >> "%CONFIG_FILE%"
echo   "data_directory": "~/.alang", >> "%CONFIG_FILE%"
echo   "debug": false >> "%CONFIG_FILE%"
echo } >> "%CONFIG_FILE%"

echo ✅ Configuration created at: %CONFIG_FILE%

REM Create desktop shortcut
echo 🖥️ Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT=%DESKTOP%\Alang.lnk

set VBSCRIPT=%TEMP%\CreateShortcut.vbs
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBSCRIPT%"
echo sLinkFile = "%SHORTCUT%" >> "%VBSCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBSCRIPT%"
echo oLink.TargetPath = "python" >> "%VBSCRIPT%"
echo oLink.Arguments = "%INSTALL_DIR%\simple_chat.py" >> "%VBSCRIPT%"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%VBSCRIPT%"
echo oLink.Description = "Alang AI Coding Assistant" >> "%VBSCRIPT%"
echo oLink.Save >> "%VBSCRIPT%"

cscript //nologo "%VBSCRIPT%"
del "%VBSCRIPT%"

echo.
echo 🎉 Alang has been installed successfully!
echo.
echo 📋 Next steps:
echo 1. Add your Gemini API key to: %CONFIG_FILE%
echo 2. Double-click the desktop shortcut "Alang"
echo 3. Or run: %INSTALL_DIR%\simple_chat.py
echo.
echo 🚀 Happy coding with Alang!
pause
