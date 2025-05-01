#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Set Python path
export PYTHONPATH=/opt/render/project/src

# Create database tables
python -c "from backend.app import create_app; from backend.models import db; app = create_app(); app.app_context().push(); db.create_all()"

# Print Python path for debugging
echo "PYTHONPATH is set to: $PYTHONPATH"
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la 