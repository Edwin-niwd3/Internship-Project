from .models import Class, Student
import difflib

def getNames(Class_Query):
  ans = []
  for Class in Class_Query:
    ans.append(Class.Course_Name)
  return ans

def get_closest_class(level, class_list):
  return difflib.get_close_matches(level, class_list, n=1)[0] if level else None

def collect_prerequisites(course, student, collected=None):
    if collected is None:
        collected = []

    # Add the current course name if it's not already in the list
    if course.Course_Name not in collected:
        if student.check_if_taken(course.Course_Name):
          collected.append(course.Course_Name)

    # Recursively collect prerequisites for this course
    for prereq in course.prerequisites:
        collect_prerequisites(prereq,student, collected)
    
    return collected

def fetch_course_with_prerequisites(course_name, student):
  """This is done to collect all prerequisites for a course by name"""
  if not course_name:
    return []
  course = Class.query.filter_by(Course_Name = course_name).first()
  if not course:
    return []
  prerequisites = collect_prerequisites(course, student)
  prerequisites.reverse()
  return prerequisites