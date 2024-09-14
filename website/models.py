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
  Course_Name = db.Column(db.String(1000))
  Course_Prerequisite = db.Column(db.String(1000))
  Course_Notes = db.Column(db.String(10000))