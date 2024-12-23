from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .reading import read

db = SQLAlchemy()
DB_NAME = "classes.db"

def create_app(test_config = None):
  app = Flask(__name__)
  app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY', 'alshffiuefnaknsdk'),
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
  )
  db.init_app(app)


  from .views import views
  from .models import Class, Student, Path, Major

  with app.app_context():
    if not os.path.exists('website/' + DB_NAME):
      db.create_all()

    data_insert(app, db, Class, Path, Major)

  app.register_blueprint(views, url_prefix = '/')

  return app

def data_insert(app, db, Class, Path, Major):
    combinedDf = read()
    if combinedDf:
        try:
            with app.app_context():
                for index, row in combinedDf[1].iterrows():
                    # Get or create the Path ID based on the 'Path' column in the data
                    path_name = row.get('Path')
                    if path_name:
                        path_id = get_or_create_path(db.session, Path, path_name)

                    # Prepare course data
                    class_data = {
                        'Course_Name': row.get('Courses'),
                        'Course_Prerequisite': row.get('Prerequisite'),
                        'Course_Notes': row.get('Notes'),
                        'Course_Path': path_id  # Use the path_id retrieved dynamically
                    }

                    if class_data['Course_Name']:
                        # Insert the course
                        course = insert_Class_if_not_exists(db.session, Class, class_data)
                        
                        # Add the prerequisites for the course
                        add_prerequisites(course, class_data['Course_Prerequisite'], db.session, Class)

                for index, row in combinedDf[0].iterrows():
                # Insert or update Major with string values for math, english, and science levels
                    major_name = row.get('Major Name')
                    math_course = row.get('Math Level')  # This is now a string
                    english_course = row.get('English Level')  # This is now a string
                    science_course = row.get('Science Level')  # This is now a string
                    major_keywords = row.get('Keywords')

                    major_data = {
                        'Major_Name': major_name,
                        'Math_Level': math_course,
                        'English_Level': english_course,
                        'Science_Level': science_course,
                        'Major_Keywords' : major_keywords
                    }
                    if major_data['Major_Name']:
                        insert_Major_if_not_exists(db.session, Major, major_data)
        except:
            pass

def insert_Class_if_not_exists(session, Class, class_data):
    course = session.query(Class).filter_by(Course_Name=class_data['Course_Name']).first()
    if course:
        course.Course_Notes = class_data.get('Course_Notes', course.Course_Notes)
        course.Course_Path = class_data.get('Course_Path', course.Course_Path)
    if not course:
        # Create a new course if it doesn't exist
        course = Class(
            Course_Name=class_data['Course_Name'],
            Course_Notes=class_data['Course_Notes'],
            Course_Path=class_data['Course_Path']  # This would be the ID from the Path model
        )
    session.add(course)
    session.commit()  # Commit to get the course ID if needed later
    return course

def add_prerequisites(course, prerequisites_str, session, Class):
    if isinstance(prerequisites_str, str) and prerequisites_str.strip():
        # Split prerequisites (if they are comma-separated)
        prerequisites_list = [p.strip() for p in prerequisites_str.split(',')]

        for prereq_name in prerequisites_list:
            # Check if prerequisite course exists, if not create it
            prereq_course = session.query(Class).filter_by(Course_Name=prereq_name).first()
            if not prereq_course:
                prereq_course = Class(Course_Name=prereq_name)
                session.add(prereq_course)
                session.commit()  # Commit to get the ID for the prerequisite course

            # Add the prerequisite to the course's prerequisites list
            if prereq_course not in course.prerequisites:
                course.prerequisites.append(prereq_course)

        session.commit()  # Commit after updating the relationships


def insert_Major_if_not_exists(session, model, data):
   if not Major_exists(session, model, **data):
      new_record = model(**data)
      session.add(new_record)
      session.commit()

def Class_exists(session, model, **data): 
    query = session.query(model).filter_by(Course_Name = data['Course_Name'])
    return query.first() is not None

def Major_exists(session, model, **data):
   query = session.query(model).filter_by(Major_Name = data['Major_Name'])
   return query.first() is not None


def get_or_create_path(session, Path, path_name):
    path = session.query(Path).filter_by(Path_Name=path_name).first()
    if not path:
        new_path = Path(Path_Name=path_name)
        session.add(new_path)
        session.commit()
        return new_path.id
    return path.id