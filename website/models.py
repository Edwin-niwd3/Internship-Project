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
    def from_dict(data):
        return Student(data['firstName'], data['lastName'], data['keywords'], data['classesTaken'])
    
    def check_if_taken(self, class_in_question):
        try:
            response = self.classesTaken[class_in_question]
            #checks if we haven't taken the class
            if not response:
                return True
            if response == '0':
                return True
            #we have already taken the class
            return False
        except KeyError:
            #know error, this means that the keyword isn't in the list, in which case auto return True
            return True

prerequisite_table = db.Table('prerequisite',
    db.Column('course_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
    db.Column('prerequisite_id', db.Integer, db.ForeignKey('class.id'), primary_key=True)
)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Course_Name = db.Column(db.String(1000))
    prerequisites = db.relationship('Class', secondary=prerequisite_table, 
                                     primaryjoin=id==prerequisite_table.c.course_id,
                                     secondaryjoin=id==prerequisite_table.c.prerequisite_id)
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