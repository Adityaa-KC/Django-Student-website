import os
import uuid
import logging
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, session, jsonify, abort, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from models import User, Application, Course
from forms import LoginForm, RegistrationForm, ApplicationForm, PreviewForm

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Helper function to check if file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']

# Helper function to save file with unique name
def save_file(file, file_type):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create a unique filename to prevent overwriting
        unique_filename = f"{file_type}_{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            
            if user.is_admin:
                return redirect(next_page or url_for('admin_dashboard'))
            return redirect(next_page or url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', form=form)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Application form route
@app.route('/application', methods=['GET', 'POST'])
@login_required
def application_form():
    # Check if user already has a pending or approved application
    existing_application = Application.query.filter_by(user_id=current_user.id).first()
    if existing_application and existing_application.status in ['Pending', 'Approved']:
        flash('You already have a pending or approved application.', 'info')
        return redirect(url_for('view_application', application_id=existing_application.id))
    
    form = ApplicationForm()
    
    # Populate course choices
    courses = Course.query.all()
    form.course.choices = [(course.name, course.name) for course in courses]
    
    # If no courses exist, create some default courses
    if not courses:
        default_courses = [
            Course(name="Computer Science", description="Bachelor's in Computer Science"),
            Course(name="Electrical Engineering", description="Bachelor's in Electrical Engineering"),
            Course(name="Mechanical Engineering", description="Bachelor's in Mechanical Engineering"),
            Course(name="Civil Engineering", description="Bachelor's in Civil Engineering"),
            Course(name="Business Administration", description="Bachelor's in Business Administration")
        ]
        db.session.bulk_save_objects(default_courses)
        db.session.commit()
        
        # Reload course choices
        courses = Course.query.all()
        form.course.choices = [(course.name, course.name) for course in courses]
    
    if form.validate_on_submit():
        try:
            # Store form data in session for preview
            session['application_data'] = {
                'full_name': form.full_name.data,
                'date_of_birth': form.date_of_birth.data.strftime('%Y-%m-%d'),
                'mobile_number': form.mobile_number.data,
                'aadhar_number': form.aadhar_number.data,
                'email': form.email.data,
                'course': form.course.data
            }
            
            # Save uploaded files
            if 'photo' in request.files and request.files['photo'].filename:
                photo_file = save_file(request.files['photo'], 'photo')
                if photo_file:
                    session['application_data']['photo_path'] = photo_file
                else:
                    flash('Error uploading photo. Please try again.', 'danger')
                    return render_template('application_form.html', form=form)
            else:
                flash('Photo is required.', 'danger')
                return render_template('application_form.html', form=form)
                
            if 'signature' in request.files and request.files['signature'].filename:
                signature_file = save_file(request.files['signature'], 'signature')
                if signature_file:
                    session['application_data']['signature_path'] = signature_file
                else:
                    flash('Error uploading signature. Please try again.', 'danger')
                    return render_template('application_form.html', form=form)
            else:
                flash('Signature is required.', 'danger')
                return render_template('application_form.html', form=form)
                
            return redirect(url_for('preview_application'))
        except Exception as e:
            logger.error(f"Error in application form submission: {str(e)}")
            flash('An error occurred while processing your form. Please try again.', 'danger')
    
    return render_template('application_form.html', form=form)

# Preview application route
@app.route('/preview', methods=['GET', 'POST'])
@login_required
def preview_application():
    if 'application_data' not in session:
        flash('Please fill out the application form first.', 'warning')
        return redirect(url_for('application_form'))
    
    # Create a temporary object with date formatted properly for display
    app_data = session['application_data'].copy()
    try:
        # Format date for display
        formatted_date = datetime.strptime(app_data['date_of_birth'], '%Y-%m-%d').strftime('%d-%m-%Y')
        app_data['date_of_birth'] = formatted_date
    except Exception as e:
        logger.error(f"Error formatting date: {str(e)}")
        # If date formatting fails, use the original
        pass
    
    form = PreviewForm()
    if form.validate_on_submit():
        if form.edit.data:
            return redirect(url_for('application_form'))
        
        if form.confirm_submit.data:
            try:
                # Create new application from session data
                original_app_data = session['application_data']
                application = Application(
                    user_id=current_user.id,
                    full_name=original_app_data['full_name'],
                    date_of_birth=datetime.strptime(original_app_data['date_of_birth'], '%Y-%m-%d').date(),
                    mobile_number=original_app_data['mobile_number'],
                    aadhar_number=original_app_data['aadhar_number'],
                    email=original_app_data['email'],
                    course=original_app_data['course'],
                    photo_path=original_app_data['photo_path'],
                    signature_path=original_app_data['signature_path']
                )
                
                db.session.add(application)
                db.session.commit()
                
                # Clear session data
                session.pop('application_data', None)
                
                flash('Your application has been submitted successfully!', 'success')
                return redirect(url_for('application_success', application_id=application.id))
            except Exception as e:
                logger.error(f"Error submitting application: {str(e)}")
                flash('An error occurred while submitting your application. Please try again.', 'danger')
                return redirect(url_for('application_form'))
    
    # Pass the data with formatted date to the template
    return render_template('preview.html', application=app_data, form=form)

# Success page route
@app.route('/success/<int:application_id>')
@login_required
def application_success(application_id):
    application = Application.query.get_or_404(application_id)
    # Check if the application belongs to the current user
    if application.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    return render_template('success.html', application=application)

# View application route
@app.route('/application/<int:application_id>')
@login_required
def view_application(application_id):
    application = Application.query.get_or_404(application_id)
    # Check if the application belongs to the current user
    if application.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    return render_template('application_detail.html', application=application)

# Admin dashboard route
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    
    applications = Application.query.all()
    return render_template('admin/dashboard.html', applications=applications)

# Admin view application route
@app.route('/admin/application/<int:application_id>', methods=['GET', 'POST'])
@login_required
def admin_view_application(application_id):
    if not current_user.is_admin:
        abort(403)
    
    application = Application.query.get_or_404(application_id)
    
    if request.method == 'POST':
        status = request.form.get('status')
        if status in ['Pending', 'Approved', 'Rejected']:
            application.status = status
            db.session.commit()
            flash(f'Application status updated to {status}', 'success')
    
    return render_template('admin/application_detail.html', application=application)

# Serve uploaded files
@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500
