"""
Stress Analyzer Web Application Runner
Simple script to start the Flask development server
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

