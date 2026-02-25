"""
Neuronet Flask Application Entry Point
This is the main entry point for running the Neuronet application.

Usage:
    python app.py                    # Run with default settings (development)
    python app.py --port 5000        # Run on custom port
    FLASK_ENV=production python app.py  # Run in production mode
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the neuronet package
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import create_app from the __init__.py in the current directory
from __init__ import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Get configuration from environment
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    
    print(f"\n{'='*60}")
    print(f"Starting Neuronet Application")
    print(f"{'='*60}")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development').upper()}")
    print(f"Server: http://{host}:{port}")
    print(f"Debug Mode: {debug}")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=debug)
