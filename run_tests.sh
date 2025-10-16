#!/bin/bash

# Test runner script for the High School Management System API

echo "Running FastAPI tests..."
echo "========================"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing -v

echo ""
echo "Test run completed!"