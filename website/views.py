from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Path, Major, Student, Class
from markupsafe import escape
from .tools import getNames, collect_prerequisites
import difflib

views = Blueprint('views', __name__)

@views.route('/', methods = ["GET","POST"])
def home():
  if request.method == "POST":
    selected_grades = {}
    keywords = request.form.getlist("keywords")
    First_Name = request.form.get("First Name")
    Last_Name = request.form.get("Last Name")

    if First_Name == None or Last_Name == None:
      flash("Missing Name", 'error')
      return redirect(request.url)
    if keywords == None:
      flash("Please select at least one key word", 'error')
      return redirect(request.url)
    paths = Path.query.all()
    course_names = []
    for path in paths:
      for course in path.classes:
        course_names.append(course.Course_Name)
    for course in course_names:
      # Retrieve the selected radio button value for each course
      selected_grade = request.form.get(f'grade-{course}')
      selected_grades[course] = selected_grade
      if selected_grade == None:
        flash(f"{course} was left unanswered", 'error')
        return redirect(request.url)
    ##print(keywords)
    keywords_str = ','.join(keywords)
    student = Student(firstName = First_Name, lastName = Last_Name, keywords= keywords_str, classesTaken=selected_grades)
    session['student'] = student.to_dict()
    return redirect(url_for('views.results', keywords = keywords_str, First_name = First_Name))
  else:    
    keywords = ['Computers', 'Math', 'Science', 'Art', 'Electricity', 'Space', 'Law', 'Police', 'Construction', 'Engineering', 'Placeholder', 'Placeholder2', 'Placeholder3', 'Placeholder4']
    paths = Path.query.all()
    return render_template('index.html', keywords = keywords, paths = paths)

@views.route('/results')
def results():
  # Get the comma-separated keywords string from the URL
  keywords_str = request.args.get('keywords')
  # Convert the string back into a list
  keywords_list = keywords_str.split(',') if keywords_str else []
  keywords_set = set(keywords_list)
  filtered_majors = {}
  majors = Major.query.all()
  for major in majors:
    major_keywords = major.Major_Keywords.strip().split(',') if major.Major_Keywords else []
    major_set = set(major_keywords)
    intersect = list(major_set & keywords_set)
    if len(intersect) > 0:
      filtered_majors.update({major.Major_Name: len(intersect)})
  #sort majors based on most amount of keywords
  sorted_dict = dict(sorted(filtered_majors.items(), key=lambda item: item[1], reverse = True))
  queries = []
  for key in sorted_dict:
    query = Major.query.filter_by(Major_Name = key).first()
    if query:
      queries.append(query)
    else:
      print(f"no query found for {key}")

  return render_template('results.html', filtered_majors = queries)

@views.route('/major/<string:major_name>')
def major(major_name):
  Major_query = Major.query.filter_by(Major_Name = major_name).first()
  ClassList = getNames(Class.query.all())
  #returns a list of close names, just take the first one
  Math_Class = difflib.get_close_matches(Major_query.Math_Level, ClassList)
  English_Class = difflib.get_close_matches(Major_query.English_Level, ClassList)
  Science_Class = difflib.get_close_matches(Major_query.Science_Level, ClassList)
  math_course = Class.query.filter_by(Course_Name = Math_Class[0]).first()
  english_course = Class.query.filter_by(Course_Name = English_Class[0]).first()
  science_course = Class.query.filter_by(Course_Name = Science_Class[0]).first()
  if math_course:
    math_prerequisites = collect_prerequisites(math_course)
    math_prerequisites.reverse()
  if english_course:
    english_prerequisites = collect_prerequisites(english_course)
    english_prerequisites.reverse()
  if science_course:
    science_prerequisites = collect_prerequisites(science_course)
    science_prerequisites.reverse()
  print(f"math prerequisites = {math_prerequisites}\nenglish prerequisites = {english_prerequisites}\nscience prerequisites = {science_prerequisites}")
  #reverse every list

  return render_template('majors.html', major = Major_query)

