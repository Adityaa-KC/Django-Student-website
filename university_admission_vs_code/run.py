"""
Run script for the University Admission System.
This script sets up the Flask application and runs it on port 5000.
"""

from main import app

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)