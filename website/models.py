from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from . import db

class Student(UserMixin):
    def __init__(self, firstName, lastName, keywords, classesTaken):
        self.firstName = firstName
        self.lastName = lastName
        self.keywords = keywords
        self.classesTaken = classesTaken
    def to_dict(self):
        return{
        'firstName': self.firstName,
        'lastName' : self.lastName,
        'keywords' : self.keywords,
        'classesTaken' : self.classesTaken
        }
    @staticmethod
    def from_dict(self, data):
        return Student(data['firstName'], data['lastName'], data['keywords'], data['classesTaken'])

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Course_Name = db.Column(db.String(1000))
    Course_Prerequisite = db.Column(db.String(1000))
    Course_Notes = db.Column(db.String(10000))
    Course_Path = db.Column(db.Integer, db.ForeignKey('path.id'))

class Path(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Path_Name = db.Column(db.String(120), unique = True)
    classes = db.relationship('Class')

class Major(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   Major_Name = db.Column(db.String(120), unique = True)
   Math_Level = db.Column(db.String(120))
   English_Level = db.Column(db.String(120))
   Science_Level = db.Column(db.String(120))
   Major_Keywords = db.Column(db.String(10000))