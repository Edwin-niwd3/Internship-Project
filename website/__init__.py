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

    with app.app_context():
        for index, row in combinedDf[1].iterrows():
            # Ensure the path exists or create a new one
            path_name = row.get('Path')
            if path_name:
              path_id = get_or_create_path(db.session, Path, path_name)

            # Create or retrieve class information
            class_data = {
                'Course_Name': row.get('Courses'),
                'Course_Prerequisite': row.get('Prerequisite'),
                'Course_Notes': row.get('Notes'),
                'Course_Path': path_id
            }
            if class_data['Course_Name']:
              insert_Class_if_not_exists(db.session, Class, class_data)

        for index, row in combinedDf[0].iterrows():
          # Insert or update Major with string values for math, english, and science levels
          major_name = row.get('Major Name')
          math_course = row.get('Math Level')  # This is now a string
          english_course = row.get('English Level')  # This is now a string
          science_course = row.get('Science Level')  # This is now a string

          major_data = {
              'Major_Name': major_name,
              'Math_Level': math_course,
              'English_Level': english_course,
              'Science_Level': science_course
          }
          print(f'major data: ', major_data)
          if major_data['Major_Name']:
            insert_Major_if_not_exists(db.session, Major, major_data)

def insert_Class_if_not_exists(session, model, data):
    if not Class_exists(session, model, **data):
        new_record = model(**data)
        session.add(new_record)
        session.commit()
        print(f"Inserted new Class: {new_record}")

def insert_Major_if_not_exists(session, model, data):
   if not Major_exists(session, model, **data):
      new_record = model(**data)
      session.add(new_record)
      session.commit()
      print(f"Inserted new Major: ", {new_record})
   else:
      print('Major Insertion Failed!!!')

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