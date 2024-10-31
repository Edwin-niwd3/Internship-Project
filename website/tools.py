from .models import Class, Student, Major
import difflib
import re

def getNames(Class_Query):
  ans = []
  for Class in Class_Query:
    ans.append(Class.Course_Name)
  return ans

def get_closest_class(level, class_list):
  try:
    return difflib.get_close_matches(level, class_list, n=1)[0] if level else None
  except:
     print(f"error at this: {level}")

def collect_prerequisites(course, student, collected=None):
    if collected is None:
        collected = []

    # Add the current course name if it's not already in the list
    if course.Course_Name not in collected:
        if student.check_if_taken(course.Course_Name):
          collected.append(course.Course_Name)
        else:
           collected.append(return_strike_through(course.Course_Name))

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

def fetch_major_keywords():
  """This is done to fetch all the possible keywords we can list to a major"""
  major_query = Major.query.all()
  keyword_set = set()
  for major in major_query:
    major_keywords = major.Major_Keywords.strip().split(',') if major.Major_Keywords else []
    #get rid of duplicates
    for keyword in major_keywords:
       if keyword not in keyword_set:
          keyword_set.add(keyword)

  return list(keyword_set)

def draw_bulleted_list(pdf, items, x, y, line_height=20):
    """Draws a bulleted list on the PDF."""
    for item in items:
        if is_strikethrough(item):
          item = remove_strikethrough(item)
          pdf.drawString(x,y,f"• {item}")
          text_width = pdf.stringWidth(item, "Helvetica", 12)
          pdf.setLineWidth(1)  # Thickness of the line
          pdf.line(x, y + 3, x + text_width, y + 3)
          y -= line_height  # Move to the next line

        else:
          pdf.drawString(x, y, f"• {item}")
          y -= line_height  # Move to the next line

def return_strike_through(text):
   """Creates a strikethrough version of a given string"""
   return ''.join(['\u0336{}'.format(c) for c in text])

def is_strikethrough(text):
    """Check if the given string contains strikethrough formatting."""
    return all(text[i] == '\u0336' for i in range(0, len(text), 2))

def remove_strikethrough(text):
    """Remove strikethrough formatting from the given string."""
    # Extract only the non-\u0336 characters (those at even indices)
    return re.sub(u'\u0336', '', text)