#!/bin/bash
set -e

echo "================================"
echo "Initializing Neuronet Database"
echo "================================"
python init_db.py

echo ""
echo "================================"
echo "Starting Neuronet Application"
echo "================================"
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 60 wsgi:app
