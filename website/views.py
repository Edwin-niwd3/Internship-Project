from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
  keywords = ['Computers', 'Math', 'Science', 'Art', 'Electricity', 'Space', 'Law', 'Police', 'Construction', 'Engineering']
  return render_template('index.html', keywords = keywords)