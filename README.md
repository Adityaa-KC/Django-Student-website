# University Admission System

A comprehensive web application for managing university admission applications with user registration, application submission, and an admin dashboard.

## Features

- User authentication (register, login, logout)
- Detailed application form for university admission
- File upload for photos and signatures
- Application preview and editing
- Application status tracking
- Admin dashboard for application management
- Responsive design

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set up environment variables (optional):
   - `DATABASE_URL`: Database connection string (default: SQLite)
   - `SESSION_SECRET`: Secret key for session security

## Running the Application

1. With the virtual environment activated, run:
   ```
   python run.py
   ```
   or use the main module directly:
   ```
   python main.py
   ```
   or use gunicorn in production:
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```
2. Open your browser and navigate to http://localhost:5000

## Admin Access

To create an admin user, run the provided script:

```
python create_admin.py
```

This will create an admin user with:
- Email: admin@example.com
- Password: adminpassword

**IMPORTANT**: Change the default password after your first login!

You can also modify the script to use custom credentials before running it.

## Project Structure

- `app.py` - Application initialization
- `main.py` - Entry point
- `run.py` - Development server script
- `config.py` - Configuration settings
- `models.py` - Database models
- `forms.py` - Form definitions using Flask-WTF
- `routes.py` - Route handlers and controllers
- `create_admin.py` - Script to create admin user
- `requirements.txt` - Required Python packages
- `static/` - Static files (CSS, JavaScript, uploads)
  - `css/` - Stylesheets
  - `js/` - JavaScript files
  - `uploads/` - Uploaded files (photos, signatures)
- `templates/` - HTML templates
  - `admin/` - Admin dashboard templates
  - `errors/` - Error page templates
- `instance/` - Instance-specific files (database)

## VS Code Integration

This project includes VS Code configuration files in the `.vscode` directory:
- `launch.json` - Run configuration
- `settings.json` - Editor settings

To run the application in VS Code:
1. Open the project folder in VS Code
2. Make sure you have the Python extension installed
3. Press F5 or use the Run menu to start the application

## License

This project is intended for educational purposes only.