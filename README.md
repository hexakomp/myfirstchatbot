# My First Chatbot

This repository contains simple chatbot scripts using different backends (Ollama, Gemini, etc.). This README explains how to set up the environment, create a `.env` file, and run the example scripts.

## Files
- `chatbot-ollama.py` — example bot using Ollama (local/remote Ollama API)
- `chatbot-gemini.py` — example bot using Google Gemini (or configured provider)
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.9+
- Git

## Setup (Windows)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

2. Install dependencies from the `requirements.txt` file:

```powershell
pip install -r .\requirements.txt
```

## .env setup

Create a file named `.env` in the repository root to store API keys and configuration.

Example `.env` template:

```
# Example .env
GOOGLE_API_KEY=your_gemini_api_key_here
OLLAMA_API_URL=http://localhost:11434
OLLAMA_API_KEY=your_ollama_api_key_here
# Add other keys or config values your scripts use
```

How to create `.env` quickly:

PowerShell:
```powershell
Set-Content -Path .env -Value "OLLAMA_API_KEY=your_ollama_api_key_here"
```

Bash / WSL:
```bash
cat > .env <<EOF
OLLAMA_API_KEY=your_ollama_api_key_here
EOF
```

How to load values in Python (recommended pattern):

```python
from dotenv import load_dotenv
import os

load_dotenv()
google_key = os.getenv('GOOGLE_API_KEY')
ollama_key = os.getenv('OLLAMA_API_KEY')
```

If you prefer environment variables without a `.env` file, set them in your shell before running the scripts.

## Running the bots

After setup and creating `.env`, run either script:

```powershell
python chatbot-ollama.py
python chatbot-gemini.py
```

Check the top of each script to see which environment variables it expects.

## Notes & Troubleshooting

- The dependency filename in this repo is `requrirements.txt` (typo). If you prefer, rename it to `requirements.txt` and update your workflows accordingly.
- If a script raises missing key errors, confirm the variable names in `.env` match those referenced in the script.
- For remote API access, ensure network access and valid API keys.

## Contributions

Feel free to open issues or PRs to improve examples and add support for more providers.
