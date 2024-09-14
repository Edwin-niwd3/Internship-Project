from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from . import db

class Student(UserMixin):
  def __init__(self, firstName, lastName, keywords):
    self.firstName = firstName
    self.lastNam = lastName
    self.keywords = keywords

class Class(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  class_name = db.Column(db.String(1000))
  class_prerequisite = db.Column(db.String(1000))