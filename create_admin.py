from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_admin_user(username="admin", email="admin@example.com", password="adminpassword"):
    """Create an admin user if one doesn't exist"""
    with app.app_context():
        # Check if admin user exists
        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.username} ({existing_admin.email})")
            return
        
        # Create new admin user
        admin = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created successfully: {username} ({email})")

if __name__ == "__main__":
    create_admin_user()
    print("You can now log in with username 'admin@example.com' and password 'adminpassword'")
    print("WARNING: Change the default password immediately after first login!")