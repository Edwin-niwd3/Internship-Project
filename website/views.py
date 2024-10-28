from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, send_file
from .models import Path, Major, Student, Class
from .tools import getNames, get_closest_class, fetch_course_with_prerequisites, fetch_major_keywords, draw_bulleted_list
from reportlab.pdfgen import canvas
from io import BytesIO
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
    ##print(keywords)
    keywords_str = ','.join(keywords)
    student = Student(firstName = First_Name, lastName = Last_Name, keywords= keywords_str, classesTaken=selected_grades)
    session['student'] = student.to_dict()
    return redirect(url_for('views.results', keywords = keywords_str, First_name = First_Name))
  else:    
    keywords = fetch_major_keywords()
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
  major_query = Major.query.filter_by(Major_Name = major_name).first()
  if not major_query:
    abort(404, description = "Major not found.")

  class_list = getNames(Class.query.all())

  subjects = {
    'Math': major_query.Math_Level,
    'English': major_query.English_Level,
    'Science': major_query.Science_Level
  }

  #iterate through each class in subjects, and get the closest match, in case some schools call it differently
  class_matches = {subject: get_closest_class(level, class_list) for subject, level in subjects.items()}


  data = session.get('student')
  print(type(data))
  student = Student.from_dict(data)

  prerequisites = {
    subject: fetch_course_with_prerequisites(course_name, student) for subject, course_name in class_matches.items()
  }

  print(f"Prerequisites: {prerequisites}")

  return render_template(
    'majors.html', math_prerequisites = prerequisites['Math'], english_prerequisites = prerequisites['English'], science_prerequisites = prerequisites['Science'], major = major_query
  )

@views.route('/download_pdf')
def download_pdf():
    # Collect student data from the form submission
    data = session.get('student')
    student_info = Student.from_dict(data)
    major_name = request.args.get('major')
    math_prerequisites = request.args.getlist('math_prerequisites')
    science_prerequisites = request.args.getlist('science_prerequisites')
    english_prerequisites = request.args.getlist('english_prerequisites')
    major = Major.query.filter_by(Major_Name = major_name).first()

    # Create a BytesIO buffer for PDF
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)

    y = 800  # Starting y-coordinate
    line_height = 20  # Adjust based on desired spacing

    pdf.drawString(100, y, "Student Information")
    y -= line_height
    pdf.drawString(100, y, f"Name: {student_info.firstName} {student_info.lastName}")
    y -= line_height
    pdf.drawString(100, y, f"Chosen Major: {major.Major_Name}")
    y -= line_height
    if major.Math_Level and major.Math_Level.strip() != "None":
      pdf.drawString(100, y, f"Highest Math Level: {major.Math_Level}")
      y -= line_height
      pdf.drawString(100, y, "Math Prerequisites:")
      y -= line_height
      draw_bulleted_list(pdf, math_prerequisites, 120, y, line_height)
      y -= line_height * len(math_prerequisites)  # Adjust for the list height
    if major.Science_Level and major.Science_Level.strip() != "None":
      pdf.drawString(100, y, f"Highest Science Level: {major.Science_Level}")
      y -= line_height
      pdf.drawString(100, y, "Science Prerequisites:")
      y -= line_height
      draw_bulleted_list(pdf, science_prerequisites, 120, y, line_height)
      y -= line_height * len(science_prerequisites)
    if major.English_Level and major.English_Level.strip() != "None":
      pdf.drawString(100, y, f"Highest English Level: {major.English_Level}")
      y -= line_height
      pdf.drawString(100, y, "English Prerequisites:")
      y -= line_height
      draw_bulleted_list(pdf, english_prerequisites, 120, y, line_height)


    # Finalize and save the PDF
    pdf.showPage()
    pdf.save()
    pdf_buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="Student_Information.pdf",
        mimetype='application/pdf'
    )
    # return "Hello!"