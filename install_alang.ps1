# PowerShell Installation Script for Alang
Write-Host "🤖 Alang Installation Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "⚠️  Running without administrator privileges. Some features may not work." -ForegroundColor Yellow
}

# Create installation directory
$installDir = "$env:USERPROFILE\alang"
Write-Host "📁 Creating installation directory: $installDir" -ForegroundColor Blue

if (!(Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

# Copy files from current directory
Write-Host "📋 Copying Alang files..." -ForegroundColor Blue
$currentDir = Get-Location
Copy-Item -Path "$currentDir\*" -Destination $installDir -Recurse -Force

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Blue
try {
    & python -m pip install textual google-generativeai python-dotenv rich --quiet
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    Write-Host "Please make sure Python and pip are installed" -ForegroundColor Yellow
    exit 1
}

# Create configuration
$configDir = "$env:USERPROFILE\.alang"
$configFile = "$configDir\config.json"

Write-Host "⚙️  Setting up configuration..." -ForegroundColor Blue

if (!(Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

$configContent = @{
    gemini_api_key = ""
    model = "models/gemini-2.5-flash"
    data_directory = "~/.alang"
    debug = $false
} | ConvertTo-Json -Depth 10

Set-Content -Path $configFile -Value $configContent
Write-Host "✅ Configuration created at: $configFile" -ForegroundColor Green

# Create desktop shortcut
Write-Host "🖥️  Creating desktop shortcut..." -ForegroundColor Blue

$desktopPath = "$env:USERPROFILE\Desktop"
$shortcutPath = "$desktopPath\Alang.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "python"
$shortcut.Arguments = "$installDir\simple_chat.py"
$shortcut.WorkingDirectory = $installDir
$shortcut.Description = "Alang AI Coding Assistant"
$shortcut.Save()

Write-Host "✅ Desktop shortcut created" -ForegroundColor Green

# Create launcher script
$launcherPath = "$installDir\run_alang.bat"
$launcherContent = "@echo off`ncd /d `"$installDir`"`npython simple_chat.py`npause"

Set-Content -Path $launcherPath -Value $launcherContent

Write-Host ""
Write-Host "🎉 Alang has been installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Blue
Write-Host "1. Add your Gemini API key to: $configFile" -ForegroundColor White
Write-Host "2. Double-click the desktop shortcut 'Alang'" -ForegroundColor White
Write-Host "3. Or run: $launcherPath" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Happy coding with Alang!" -ForegroundColor Green

# Ask if user wants to run Alang now
$runNow = Read-Host "Would you like to run Alang now? (Y/N)"
if ($runNow -eq 'Y' -or $runNow -eq 'y') {
    Write-Host "🚀 Starting Alang..." -ForegroundColor Green
    & python "$installDir\simple_chat.py"
}
