#!/bin/bash
# Build script for Render deployment

set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Import articles from JSON
python manage.py import_articles || true

# Create superuser using custom command
python manage.py create_admin
