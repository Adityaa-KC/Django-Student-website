# University Admission System - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [User Registration and Login](#user-registration-and-login)
3. [Submitting an Application](#submitting-an-application)
4. [Viewing and Tracking Applications](#viewing-and-tracking-applications)
5. [Admin Dashboard](#admin-dashboard)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements
- Python 3.7 or higher
- Web browser (Chrome, Firefox, Edge, or Safari recommended)
- Internet connection for external dependencies

### Installation
1. Extract the `university_admission_system.zip` file to a location of your choice
2. Open a terminal/command prompt and navigate to the extracted folder
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

### Running the Application
1. With the virtual environment activated, run: `python run.py`
2. Open your web browser and navigate to `http://localhost:5000`
3. You should see the University Admission System home page

## User Registration and Login

### Registering a New Account
1. Click on "Register" in the navigation menu
2. Fill in the registration form:
   - Username (4-25 characters)
   - Email address (must be valid format)
   - Password (minimum 8 characters)
   - Confirm password
3. Click "Register" to create your account
4. You will be redirected to the login page after successful registration

### Logging In
1. Click on "Login" in the navigation menu
2. Enter your email address and password
3. Click "Login"
4. Upon successful login, you will be redirected to the home page

### Logging Out
1. Click on your username in the top right corner
2. Select "Logout" from the dropdown menu

## Submitting an Application

### Starting a New Application
1. Login to your account
2. Click on "Apply Now" on the home page or in the navigation menu
3. You will be taken to the application form

### Filling Out the Application Form
1. Complete all required fields in the form:
   - Personal Information (name, date of birth, contact details)
   - Educational Qualifications
   - Course Selection
   - Upload required documents (photo and signature)
2. Ensure that uploaded files meet the requirements:
   - Accepted formats: JPG, JPEG, PNG
   - Maximum file size: 10MB

### Previewing Your Application
1. After completing the form, click "Preview Application"
2. Review all information carefully
3. If you need to make changes, click "Edit Application"
4. When satisfied with your application, click "Submit Application"

### Submission Confirmation
1. After submission, you will receive a confirmation page with your application ID
2. You can print this page for your records by clicking "Print Application"

## Viewing and Tracking Applications

### Checking Application Status
1. Login to your account
2. Your application(s) will be listed on your dashboard
3. Each application will show its current status:
   - Pending: Application is under review
   - Approved: Application has been accepted
   - Rejected: Application has been declined

### Viewing Application Details
1. From your dashboard, click on "View Details" next to the application
2. This will show all details of your application

## Admin Dashboard

### Accessing Admin Panel
1. Login with admin credentials
   - Default email: admin@example.com
   - Default password: adminpassword
2. You will automatically be redirected to the admin dashboard

### Managing Applications
1. All submitted applications are listed in the admin dashboard
2. Click on an application to view its details
3. Use the action buttons to:
   - Approve an application
   - Reject an application
   - Print the application

### User Management
1. The admin dashboard allows viewing all registered users
2. User accounts can be managed as needed

## Troubleshooting

### Common Issues

#### Login Problems
- Ensure you are using the correct email and password
- Check if Caps Lock is enabled
- Try resetting your password if you've forgotten it

#### File Upload Issues
- Verify that your files are in the correct format (JPG, JPEG, PNG)
- Ensure files are under the 10MB size limit
- Try uploading a different file if problems persist

#### Application Not Submitting
- Check that all required fields are completed
- Ensure you have clicked "Submit Application" after preview
- Try clearing your browser cache and trying again

### Getting Help
If you encounter any issues not covered in this guide, please contact the system administrator for assistance.