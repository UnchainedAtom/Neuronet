"""
WSGI entry point for production deployment

This file is used by production WSGI servers like Gunicorn or uWSGI.

Usage with Gunicorn:
    gunicorn --bind 0.0.0.0:8000 wsgi:app

Usage with uWSGI:
    uwsgi --http :8000 --wsgi-file wsgi.py --callable app
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

from __init__ import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

