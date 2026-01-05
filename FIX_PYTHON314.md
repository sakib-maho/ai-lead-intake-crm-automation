# Fix for Python 3.14 Compatibility Issue

## Problem
Python 3.14.0 is very new and `pydantic-core==2.14.6` doesn't have pre-built wheels for it, causing build failures.

## Solutions

### Option 1: Use Python 3.11 or 3.12 (RECOMMENDED)

```bash
# Remove existing venv
rm -rf venv

# Create new venv with Python 3.12 (or 3.11)
python3.12 -m venv venv
# OR: python3.11 -m venv venv

# Activate and install
source venv/bin/activate
pip install -r requirements.txt
```

### Option 2: Use Updated Requirements (for Python 3.14)

The `requirements.txt` has been updated with newer versions. Try:

```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 3: Install Latest Versions

```bash
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn[standard] pydantic pydantic-settings httpx python-dotenv
```

This will install the latest versions which may have Python 3.14 support.

## Check Python Version

```bash
python3 --version
# If it shows 3.14, consider using 3.12 instead
```

