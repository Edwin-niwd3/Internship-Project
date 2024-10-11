from .models import Class

def getNames(Class_Query):
  ans = []
  for Class in Class_Query:
    ans.append(Class.Course_Name)
  return ans

def getPrerequisets(Course_Name):
  course = Class.query.filter_by(Course_Name = Course_Name).first()

  if not course:
    return []
  
  if not course.Course_Prerequisite:
    return []
  
  prerequisites = course.Course_Prerequisite.split(',')

  all_prerequisets = []

  for prereq in prerequisites:
    prereq = prereq.strip()
    all_prerequisets.append(prereq)
    all_prerequisets.extend(getPrerequisets(prereq))
  
  return all_prerequisets