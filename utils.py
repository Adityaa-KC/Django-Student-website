import os
import uuid
from werkzeug.utils import secure_filename
from app import app

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']

def save_file(file, file_type):
    """Save file with a unique filename and return the path"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create a unique filename to prevent overwriting
        unique_filename = f"{file_type}_{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

def validate_file_size(file):
    """Validate that the file size is under the maximum allowed size"""
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    max_size = app.config['MAX_CONTENT_LENGTH']
    return file_size <= max_size
