from datetime import datetime
import os
import secrets
from PIL import Image
from io import BytesIO

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, app, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to applications
    applications = db.relationship('Application', backref='applicant', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in years
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship to applications
    applications = db.relationship('Application', backref='course', lazy=True)
    
    def __repr__(self):
        return f"Course('{self.name}', '{self.code}', {self.duration} years)"


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(10), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    
    # Personal information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)  # M, F, O
    mobile_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    aadhar_number = db.Column(db.String(12), nullable=False)
    
    # Application status and timestamps
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    is_complete = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Uploaded documents
    photo_filename = db.Column(db.String(100), nullable=True)
    signature_filename = db.Column(db.String(100), nullable=True)
    aadhar_card_filename = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f"Application('{self.application_id}', '{self.first_name} {self.last_name}')"
    
    def save_photo(self, photo):
        return self._save_image(photo, 'photos', (300, 300))
    
    def save_signature(self, signature):
        return self._save_image(signature, 'signatures', (400, 200))
    
    def save_aadhar_card(self, aadhar_card):
        return self._save_image(aadhar_card, 'aadhar_cards')
    
    def _save_image(self, image_file, subfolder, resize=None):
        """Save image to the uploads folder with a secure filename"""
        # Generate random filename with original extension
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(image_file.filename)
        filename = random_hex + f_ext
        
        # Ensure uploads subfolder exists
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        
        file_path = os.path.join(upload_path, filename)
        
        # If resize dimensions are provided, resize the image
        if resize:
            # Open image and resize it
            img = Image.open(image_file)
            
            # If image is not in RGB mode, convert it
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize the image
            img.thumbnail(resize)
            
            # Save the resized image
            img.save(file_path)
        else:
            # Save the original image
            image_file.save(file_path)
        
        return filename
    
    def get_photo_url(self):
        if self.photo_filename:
            return os.path.join('/static/uploads/photos', self.photo_filename)
        return None
    
    def get_signature_url(self):
        if self.signature_filename:
            return os.path.join('/static/uploads/signatures', self.signature_filename)
        return None
    
    def get_aadhar_card_url(self):
        if self.aadhar_card_filename:
            return os.path.join('/static/uploads/aadhar_cards', self.aadhar_card_filename)
        return None
    
    @staticmethod
    def generate_application_id():
        """Generate a unique application ID"""
        timestamp = datetime.utcnow().strftime('%y%m%d')
        random_suffix = secrets.token_hex(2).upper()
        return f"A{timestamp}{random_suffix}"