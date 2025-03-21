#!/bin/bash
# setup.sh - Quick setup script for Enchante

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install the package in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov

# Check for required external tools
echo "Checking for required external tools..."
enchante list-tools

echo "Setup complete! You can now use 'enchante' command."

