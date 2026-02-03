@echo off
echo 🤖 Alang AI Coding Assistant
echo ============================
echo.
echo ⚠️  Please set your Gemini API key first:
echo    1. Get API key from: https://makersuite.google.com/app/apikey
echo    2. Set environment variable: set GEMINI_API_KEY=your-key-here
echo    3. Or edit: ~/.alang/config.json
echo.
set GEMINI_API_KEY=
cd /d "C:\Users\kranthi\alang"
python simple_chat.py
pause
