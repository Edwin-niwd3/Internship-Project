from flask import Flask
import os

def create_app(test_config = None):
  app = Flask(__name__)
  app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY', 'alshffiuefnaknsdk')
  )

  from .views import views
  ##from .models import models

  app.register_blueprint(views, url_prefix = '/')

  return app