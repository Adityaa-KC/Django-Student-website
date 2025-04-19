# University Admission System

A complete Flask-based university admission system with user authentication, application forms, document uploads, and admin dashboard.

## Setup Instructions

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   flask run
   ```
   or
   ```
   python main.py
   ```

5. Access the application at http://localhost:5000

## Default Admin Credentials

- Username: admin
- Password: adminpassword

## Features

- User registration and authentication
- Student application form with validation
- Document upload (photo, signature, Aadhar card)
- Application preview and print functionality
- Admin dashboard for managing applications
- Course management system

## Technologies Used

- Flask
- SQLite
- Bootstrap 5
- Font Awesome
- JavaScript