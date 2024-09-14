import pandas as pd
import os

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