#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Set Python path
export PYTHONPATH=/opt/render/project/src

# Initialize database and create admin user
python backend/init_db.py

# Print Python path for debugging
echo "PYTHONPATH is set to: $PYTHONPATH"
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la 