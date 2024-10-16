from .models import Class

def getNames(Class_Query):
  ans = []
  for Class in Class_Query:
    ans.append(Class.Course_Name)
  return ans

def collect_prerequisites(course, collected=None):
    if collected is None:
        collected = []

    # Add the current course name if it's not already in the list
    if course.Course_Name not in collected:
        collected.append(course.Course_Name)

    # Recursively collect prerequisites for this course
    for prereq in course.prerequisites:
        collect_prerequisites(prereq, collected)
    
    return collected