from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

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
  from .models import models

  app.register_blueprint(views, url_prefix = '/')

  return app