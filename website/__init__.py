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
  from .models import Class, Student, Path

  with app.app_context():
    if not os.path.exists('website/' + DB_NAME):
      db.create_all()

  data_insert(app, db, Class, Path)

  app.register_blueprint(views, url_prefix = '/')

  return app

def data_insert(app, db, Class, Path):
    combinedDf = read()

    with app.app_context():
        for index, row in combinedDf.iterrows():
            # Ensure the path exists or create a new one
            path_name = row.get('Path')
            path_id = get_or_create_path(db.session, Path, path_name)

            data = {
                'Course_Name': row.get('Courses'),
                'Course_Prerequisite': row.get('Prererequisite'),
                'Course_Notes': row.get('Notes'),
                'Course_Path': path_id
            }
            insert_data_if_not_exists(db.session, Class, data)

def insert_data_if_not_exists(session, model, data):
  if not record_exists(session, model, **data):
    new_record = model(**data)
    session.add(new_record)
    session.commit()
    print(f"Inserted new record: {new_record}")

def record_exists(session, model, **data):
  query = session.query(model).filter_by(Course_Name = data['Course_Name'])
  result = query.first() is not None
  return result

def get_or_create_path(session, Path, path_name):
    path = session.query(Path).filter_by(Path_Name=path_name).first()
    if not path:
        new_path = Path(Path_Name=path_name)
        session.add(new_path)
        session.commit()
        return new_path.id
    return path.id