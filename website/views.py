from flask import Blueprint, render_template, request, redirect, url_for
from .models import Path


views = Blueprint('views', __name__)

@views.route('/', methods = ["GET","POST"])
def home():
  if request.method == "POST":
    keywords = request.form.getlist("keywords")
    First_Name = request.form.get("First Name")
    Last_Name = request.form.get("Last Name")
    English_Level = request.form.get("English Level")
    Math_Level = request.form.get("Math Level")
    ##print(keywords)
    print(First_Name, Last_Name, English_Level, Math_Level)
    keywords_str = ','.join(keywords)
    return redirect(url_for('views.results', keywords = keywords_str, First_name = First_Name))
  else:    
    keywords = ['Computers', 'Math', 'Science', 'Art', 'Electricity', 'Space', 'Law', 'Police', 'Construction', 'Engineering', 'Placeholder', 'Placeholder2', 'Placeholder3', 'Placeholder4']
    paths = Path.query.all()
    return render_template('index.html', keywords = keywords, paths = paths)

@views.route('/results')
def results():
  example_majors = {
    'Computer Science' : ['Computers, Electricity, Science, Math, Engineering'],
    'Construction':['Computers', 'Engineering', 'Math', 'Construction'],
    'Animation':['Computers', 'Art'],
    'Law Enforcment':['Law', 'Police'],
    'Astronaught': ['Science', 'Space', 'Engineering']
  }
  # Get the comma-separated keywords string from the URL
  keywords_str = request.args.get('keywords')
  # Convert the string back into a list
  keywords_list = keywords_str.split(',') if keywords_str else []
  keywords_set = set(keywords_list)
  filtered_majors = {}
  for major, keywords in example_majors.items():
    if any(keyword in keywords_set for keyword in keywords):
      filtered_majors[major] = keywords

  return render_template('results.html', majors = filtered_majors)