from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Path, Major, Student


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
    filtered_majors.update({major.Major_Name: len(intersect)})
  #sort majors based on most amount of keywords
  sorted_dict = dict(sorted(filtered_majors.items(), key=lambda item: item[1]))
  print(sorted_dict)

  return render_template('results.html', filtered_majors = filtered_majors)