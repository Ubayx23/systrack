#!/bin/bash
# SysTrack Setup Script
# This script sets up a virtual environment and installs dependencies

set -e  # Exit on error

echo "SysTrack Setup Script"
echo "===================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if we're already in a virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Note: You're already in a virtual environment: $VIRTUAL_ENV"
    echo "Installing dependencies in current environment..."
    pip install -r requirements.txt
    echo ""
    echo "Setup complete! You can now run:"
    echo "  python src/systrack.py --summary"
    exit 0
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To use SysTrack:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run SysTrack Web App:"
echo "     python app.py"
echo "     Then open http://localhost:5000 in your browser"
echo ""
echo "  Or use the CLI:"
echo "     python src/systrack.py --summary"
echo ""
echo "  3. When done, deactivate:"
echo "     deactivate"
echo ""

