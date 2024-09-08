from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

class Student(UserMixin):
  def __init__(self, firstName, lastName, keywords):
    self.firstName = firstName
    self.lastNam = lastName
    self.keywords = keywords

class Major(db.Model):
  ...