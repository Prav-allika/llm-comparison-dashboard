#!/bin/bash
# ==============================================
# LLM Dashboard - Setup Script
# Run once to create the environment and install dependencies
# Usage: bash setup.sh
# ==============================================

set -e  # stop on first error

echo "Setting up LLM Evaluation Dashboard..."

# --- Step 1: Check Python version ---
PYTHON=$(command -v python3 || command -v python)
PY_VERSION=$($PYTHON --version 2>&1)
echo "Using $PY_VERSION"

# --- Step 2: Create virtual environment ---
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists, skipping creation."
fi

# --- Step 3: Activate virtual environment ---
echo "Activating virtual environment..."
source venv/bin/activate

# --- Step 4: Upgrade pip ---
pip install --upgrade pip --quiet

# --- Step 5: Install dependencies ---
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To run the app:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open: http://127.0.0.1:7860"
