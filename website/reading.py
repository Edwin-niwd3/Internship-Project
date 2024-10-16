import pandas as pd
import os

def read():
    folder_path = 'data'
    
    all_lists = []  # Master list to hold lists from each file
    try:
      for filename in os.listdir(folder_path):
          if filename.endswith('.xlsx') or filename.endswith('.xls'):
              file_path = os.path.join(folder_path, filename)
              df = pd.read_excel(file_path)
              
              # Convert dataframe to list and append to the master list
              all_lists.append(df)
      return all_lists
    except:
       return None

def main():
  test = read()
  print(test[0])

if __name__ == "__main__":
  main()