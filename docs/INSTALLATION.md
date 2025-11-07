# Installation Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git
- (Optional) Docker and Docker Compose

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/learnaikid-collab/iRESARCH-LABs.git
cd iRESARCH-LABs
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn (web framework)
- Google Generative AI SDK (for Gemini 2.5 Flash)
- Pydantic (data validation)
- PyYAML (configuration)
- Testing tools (pytest)
- And other required packages

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Google API key
nano .env  # or use your preferred editor
```

Required configuration:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### 5. Verify Installation

```bash
python verify_installation.py
```

This script tests all core components without requiring an API key.

### 6. Run the Application

```bash
python run.py
```

Or directly:
```bash
python -m src.web.backend
```

The application will start on `http://localhost:8000`.

## Docker Installation (Alternative)

### Using Docker Compose

```bash
# 1. Create .env file with your API key
cp .env.example .env
# Edit .env to add GOOGLE_API_KEY

# 2. Build and run
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Stop
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t apos:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key_here \
  --name apos \
  apos:latest

# View logs
docker logs -f apos

# Stop container
docker stop apos
docker rm apos
```

## Troubleshooting

### Import Errors

If you get import errors:
```bash
# Ensure you're in the project root directory
cd /path/to/iRESARCH-LABs

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Google API Key Issues

1. Verify your API key is correct
2. Check if the API is enabled in Google Cloud Console
3. Ensure you have sufficient quota

Test the API key:
```python
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")
response = model.generate_content("Hello!")
print(response.text)
```

### Port Already in Use

If port 8000 is already in use:

```bash
# Change port in .env file
APP_PORT=8080

# Or set environment variable
export APP_PORT=8080
python run.py
```

### Module Not Found Errors

Ensure you're running from the project root and the virtual environment is activated:

```bash
# Check current directory
pwd  # Should show .../iRESARCH-LABs

# Verify virtual environment
which python  # Should show .../venv/bin/python

# If not activated, activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

## Development Setup

For development, install additional tools:

```bash
# Install development dependencies
pip install black flake8 mypy isort

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest --cov=src tests/
```

## Platform-Specific Notes

### Linux

Should work out of the box with Python 3.9+.

### macOS

May need to install Python via Homebrew:
```bash
brew install python@3.11
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Ensure "Add Python to PATH" is checked during installation
3. Use Command Prompt or PowerShell
4. Replace `source venv/bin/activate` with `venv\Scripts\activate`

## Minimal Installation (Core Components Only)

If you only want to use the core components without the web interface:

```bash
# Install minimal dependencies
pip install pydantic pyyaml google-generativeai

# Use the components directly in Python
python
>>> from src.core import TaskAnalyzer, PromptBuilder
>>> analyzer = TaskAnalyzer()
>>> analysis = analyzer.analyze("Your request here")
```

## Verifying Installation

Run the verification script:
```bash
python verify_installation.py
```

You should see:
```
✅ All component tests passed!
```

If any tests fail, check the error messages for specific issues.

## Next Steps

After installation:

1. **Read the Documentation**
   - [API Reference](docs/API.md)
   - [Usage Examples](docs/USAGE.md)

2. **Try the Web Interface**
   - Navigate to http://localhost:8000
   - Try optimizing a prompt
   - Explore the API docs at http://localhost:8000/docs

3. **Run Examples**
   - See `docs/USAGE.md` for code examples
   - Try different optimization strategies

4. **Configure Settings**
   - Edit `config/optimization.yaml` for algorithm parameters
   - Edit `config/safety.yaml` for safety settings
   - Edit `config/models.yaml` for model configurations

## Getting Help

- Check [GitHub Issues](https://github.com/learnaikid-collab/iRESARCH-LABs/issues)
- Read the documentation in the `docs/` folder
- Review example code in `docs/USAGE.md`
