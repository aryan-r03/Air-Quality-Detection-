#!/bin/bash

# Air Quality Prediction App - Startup Script

echo "=================================="
echo "Air Quality Prediction System"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Run the application
echo ""
echo "Starting Flask application..."
echo ""
python app.py
