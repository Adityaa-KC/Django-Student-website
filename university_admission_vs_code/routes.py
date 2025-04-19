import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, abort, jsonify, send_file
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app import app, db
from models import User, Course, Application


# Helper functions
def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Routes
@app.route('/')
def home():
    courses = Course.query.filter_by(is_active=True).all()
    return render_template('home.html', courses=courses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate input
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please use a different one.', 'danger')
            return render_template('register.html')
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Get user's applications
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.date_created.desc()).all()
    
    return render_template('dashboard.html', applications=applications)


@app.route('/application/new', methods=['GET', 'POST'])
@login_required
def new_application():
    if current_user.is_admin:
        flash('Admin users cannot create applications.', 'warning')
        return redirect(url_for('admin_dashboard'))
    
    # Check if user already has applications
    existing_applications = Application.query.filter_by(
        user_id=current_user.id, 
        is_complete=False
    ).first()
    
    if existing_applications:
        flash('You have an incomplete application. Please complete it first.', 'info')
        return redirect(url_for('edit_application', application_id=existing_applications.application_id))
    
    courses = Course.query.filter_by(is_active=True).all()
    
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date()
        gender = request.form.get('gender')
        mobile_number = request.form.get('mobile_number')
        email = request.form.get('email')
        aadhar_number = request.form.get('aadhar_number')
        course_id = request.form.get('course_id')
        
        # Create new application
        application_id = Application.generate_application_id()
        new_application = Application(
            application_id=application_id,
            user_id=current_user.id,
            course_id=course_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            mobile_number=mobile_number,
            email=email,
            aadhar_number=aadhar_number
        )
        
        # Save photo if uploaded
        if 'photo' in request.files and request.files['photo'].filename:
            photo = request.files['photo']
            if allowed_file(photo.filename):
                filename = new_application.save_photo(photo)
                new_application.photo_filename = filename
        
        # Save signature if uploaded
        if 'signature' in request.files and request.files['signature'].filename:
            signature = request.files['signature']
            if allowed_file(signature.filename):
                filename = new_application.save_signature(signature)
                new_application.signature_filename = filename
        
        # Save aadhar card if uploaded
        if 'aadhar_card' in request.files and request.files['aadhar_card'].filename:
            aadhar_card = request.files['aadhar_card']
            if allowed_file(aadhar_card.filename):
                filename = new_application.save_aadhar_card(aadhar_card)
                new_application.aadhar_card_filename = filename
        
        db.session.add(new_application)
        db.session.commit()
        
        flash('Application created successfully!', 'success')
        return redirect(url_for('application_preview', application_id=application_id))
    
    return render_template('application_form.html', courses=courses)


@app.route('/application/<application_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_application(application_id):
    application = Application.query.filter_by(application_id=application_id).first_or_404()
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    # Check if the application is already complete and submitted
    if application.is_complete:
        flash('This application has already been submitted and cannot be edited.', 'warning')
        return redirect(url_for('application_preview', application_id=application_id))
    
    courses = Course.query.filter_by(is_active=True).all()
    
    if request.method == 'POST':
        # Update application data
        application.first_name = request.form.get('first_name')
        application.last_name = request.form.get('last_name')
        application.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date()
        application.gender = request.form.get('gender')
        application.mobile_number = request.form.get('mobile_number')
        application.email = request.form.get('email')
        application.aadhar_number = request.form.get('aadhar_number')
        application.course_id = request.form.get('course_id')
        
        # Update photo if uploaded
        if 'photo' in request.files and request.files['photo'].filename:
            photo = request.files['photo']
            if allowed_file(photo.filename):
                filename = application.save_photo(photo)
                application.photo_filename = filename
        
        # Update signature if uploaded
        if 'signature' in request.files and request.files['signature'].filename:
            signature = request.files['signature']
            if allowed_file(signature.filename):
                filename = application.save_signature(signature)
                application.signature_filename = filename
        
        # Update aadhar card if uploaded
        if 'aadhar_card' in request.files and request.files['aadhar_card'].filename:
            aadhar_card = request.files['aadhar_card']
            if allowed_file(aadhar_card.filename):
                filename = application.save_aadhar_card(aadhar_card)
                application.aadhar_card_filename = filename
        
        db.session.commit()
        
        flash('Application updated successfully!', 'success')
        return redirect(url_for('application_preview', application_id=application_id))
    
    return render_template('application_form.html', application=application, courses=courses)


@app.route('/application/<application_id>/preview')
@login_required
def application_preview(application_id):
    application = Application.query.filter_by(application_id=application_id).first_or_404()
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    return render_template('application_preview.html', application=application)


@app.route('/application/<application_id>/submit', methods=['POST'])
@login_required
def submit_application(application_id):
    application = Application.query.filter_by(application_id=application_id).first_or_404()
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id:
        abort(403)
    
    # Check if the application is already complete and submitted
    if application.is_complete:
        flash('This application has already been submitted.', 'warning')
        return redirect(url_for('application_preview', application_id=application_id))
    
    # Check if all required files are uploaded
    if not all([application.photo_filename, application.signature_filename, application.aadhar_card_filename]):
        flash('Please upload all required documents before submitting.', 'danger')
        return redirect(url_for('edit_application', application_id=application_id))
    
    # Update application status and mark as complete
    application.is_complete = True
    application.date_updated = datetime.utcnow()
    db.session.commit()
    
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('application_success', application_id=application_id))


@app.route('/application/<application_id>/success')
@login_required
def application_success(application_id):
    application = Application.query.filter_by(application_id=application_id).first_or_404()
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    return render_template('application_success.html', application=application)


@app.route('/application/<application_id>/print')
@login_required
def application_print(application_id):
    application = Application.query.filter_by(application_id=application_id).first_or_404()
    
    # Check if the application belongs to the current user
    if application.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    return render_template('application_print.html', application=application)


# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin dashboard.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get application counts by status
    pending_count = Application.query.filter_by(status='Pending').count()
    approved_count = Application.query.filter_by(status='Approved').count()
    rejected_count = Application.query.filter_by(status='Rejected').count()
    total_count = Application.query.count()
    
    # Get recent applications
    recent_applications = Application.query.order_by(Application.date_created.desc()).limit(10).all()
    
    return render_template(
        'admin/dashboard.html',
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count,
        total_count=total_count,
        recent_applications=recent_applications
    )


@app.route('/admin/applications')
@login_required
def admin_applications():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get filter parameters
    status = request.args.get('status', '')
    course_id = request.args.get('course_id', '')
    
    # Build query
    query = Application.query
    
    if status:
        query = query.filter_by(status=status)
    
    if course_id and course_id.isdigit():
        query = query.filter_by(course_id=int(course_id))
    
    # Get all applications with filters
    applications = query.order_by(Application.date_created.desc()).all()
    
    # Get all courses for filter dropdown
    courses = Course.query.all()
    
    return render_template(
        'admin/applications.html',
        applications=applications,
        courses=courses,
        current_status=status,
        current_course_id=course_id
    )


@app.route('/admin/application/<application_id>')
@login_required
def admin_application_detail(application_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    
    application = Application.query.filter_by(application_id=application_id).first_or_404()
    
    return render_template('admin/application_detail.html', application=application)


@app.route('/admin/application/<application_id>/update-status', methods=['POST'])
@login_required
def update_application_status(application_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('dashboard'))
    
    application = Application.query.filter_by(application_id=application_id).first_or_404()
    
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Approved', 'Rejected']:
        application.status = new_status
        application.date_updated = datetime.utcnow()
        db.session.commit()
        
        flash(f'Application status updated to {new_status}.', 'success')
    else:
        flash('Invalid status value.', 'danger')
    
    return redirect(url_for('admin_application_detail', application_id=application_id))


@app.route('/admin/courses')
@login_required
def admin_courses():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    
    courses = Course.query.all()
    
    return render_template('admin/courses.html', courses=courses)


@app.route('/admin/course/new', methods=['GET', 'POST'])
@login_required
def new_course():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        duration = request.form.get('duration')
        description = request.form.get('description')
        is_active = 'is_active' in request.form
        
        # Check if course code already exists
        existing_course = Course.query.filter_by(code=code).first()
        if existing_course:
            flash('Course code already exists. Please use a different code.', 'danger')
            return redirect(url_for('new_course'))
        
        new_course = Course(
            name=name,
            code=code,
            duration=duration,
            description=description,
            is_active=is_active
        )
        
        db.session.add(new_course)
        db.session.commit()
        
        flash('Course added successfully!', 'success')
        return redirect(url_for('admin_courses'))
    
    return render_template('admin/course_form.html')


@app.route('/admin/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard'))
    
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        course.name = request.form.get('name')
        course.code = request.form.get('code')
        course.duration = request.form.get('duration')
        course.description = request.form.get('description')
        course.is_active = 'is_active' in request.form
        
        db.session.commit()
        
        flash('Course updated successfully!', 'success')
        return redirect(url_for('admin_courses'))
    
    return render_template('admin/course_form.html', course=course)


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500