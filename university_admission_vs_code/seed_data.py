"""
Seed data script for the university admission system.
This will add some initial courses to the database.
"""

from app import app, db
from models import Course

def seed_courses():
    """Add initial courses to the database"""
    courses_data = [
        {
            'name': 'Computer Science',
            'code': 'CS101',
            'duration': 4,
            'description': 'A comprehensive program covering programming, algorithms, data structures, and software engineering principles.',
            'is_active': True
        },
        {
            'name': 'Electrical Engineering',
            'code': 'EE101',
            'duration': 4,
            'description': 'Study of electrical systems, circuits, and power distribution with hands-on laboratory experience.',
            'is_active': True
        },
        {
            'name': 'Business Administration',
            'code': 'BA101',
            'duration': 3,
            'description': 'Learn business management, finance, marketing, and entrepreneurship skills for the modern business world.',
            'is_active': True
        },
        {
            'name': 'Psychology',
            'code': 'PSY101',
            'duration': 3,
            'description': 'Explore human behavior, cognitive processes, and psychological theories through research and practice.',
            'is_active': True
        },
        {
            'name': 'Mechanical Engineering',
            'code': 'ME101',
            'duration': 4,
            'description': 'Study of mechanical systems, thermodynamics, materials science, and design principles.',
            'is_active': True
        }
    ]
    
    # Check if courses already exist to avoid duplicates
    existing_codes = {course.code for course in Course.query.all()}
    
    for course_data in courses_data:
        if course_data['code'] not in existing_codes:
            course = Course(**course_data)
            db.session.add(course)
    
    db.session.commit()
    print(f"Added {len(courses_data)} courses to the database")

if __name__ == '__main__':
    with app.app_context():
        seed_courses()