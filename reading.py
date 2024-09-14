import pandas as pd
import os

class Course:
  def __init__(self, name, prerequisite = None):
    self.name = name
    self.prerequisite = prerequisite

  def get_prereqiosotes(self):
    if self.prerequisite:
      return [self.prerequisite.name] + self.prerequisite.get_prerequisites()
    else:
      return []
    
  def __repr__(self):
    return self.name

def read():
  folder_path = 'data'
  dfs = []
  for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
      file_path = os.path.join(folder_path, filename)
      df = pd.read_excel(file_path)
      dfs.append(df)

  combined_df = pd.concat(dfs, ignore_index = True)

  return combined_df


def main():
  test = read()
  print(test)


if __name__ == "__main__":
  main()