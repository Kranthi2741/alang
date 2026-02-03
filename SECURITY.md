# 🔐 Security Information

## API Key Security

**⚠️ IMPORTANT:** Never commit your Gemini API key to version control!

### How to Securely Configure Your API Key

#### Option 1: Environment Variable (Recommended)
```bash
# Linux/macOS
export GEMINI_API_KEY="your-api-key-here"

# Windows
set GEMINI_API_KEY=your-api-key-here
# Or for permanent:
setx GEMINI_API_KEY "your-api-key-here"
```

#### Option 2: Configuration File
Create `~/.alang/config.json`:
```json
{
  "gemini_api_key": "your-api-key-here",
  "model": "models/gemini-2.5-flash",
  "data_directory": "~/.alang",
  "debug": false
}
```

#### Option 3: Environment File
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
GEMINI_API_KEY=your-api-key-here
```

### Security Best Practices

1. **Never commit API keys** to Git repositories
2. **Use environment variables** whenever possible
3. **Add `.env` to `.gitignore`** (already done)
4. **Rotate API keys** regularly if you suspect compromise
5. **Use different keys** for different environments

### Getting Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and configure it using one of the methods above

### If Your API Key is Exposed

If you accidentally commit an API key:
1. **Delete the key immediately** from Google AI Studio
2. **Create a new API key**
3. **Remove the key from your Git history**
4. **Rotate the key** in all your applications

### Git Commands to Remove Committed Keys

```bash
# Remove sensitive file from history
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch filename-with-key' --prune-empty --tag-name-filter cat -- --all

# Force push to remote
git push origin --force --all
```

## Reporting Security Issues

If you find a security vulnerability in Alang, please report it privately:
- Email: security@example.com
- GitHub: Use private vulnerability reporting

Thank you for helping keep Alang secure! 🛡️
