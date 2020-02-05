import os
import shutil
import pandas as pd
import csv

def load_csv(path, delimiter):
    df = pd.read_csv(path, sep=delimiter  , engine='python')
    return df

def load_txt_file(head_path, path):
    with open(os.path.join(head_path, path), 'r') as content_file:
        content = content_file.read()
        return content

def removeEmptyFolders(path, removeRoot=True):
    'Function to remove empty folders'
    if not os.path.isdir(path):
      return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
      for f in files:
        fullpath = os.path.join(path, f)
        if os.path.isdir(fullpath):
          removeEmptyFolders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeRoot:
      print("Removing empty folder:", path)
      os.rmdir(path)

def remove_extra_data(directory, fileing_type):
    files = os.listdir(directory)

    for f in files:
        m_file = directory + "/" + f + "/" + fileing_type
        sub_files = os.listdir(m_file)
        for sub_file in sub_files:
            vals = sub_file.split("-")
            file_name = "sec_10k_" + str(vals[1]) + ".txt"
            os.rename(m_file + "/" + sub_file, m_file + "/" + file_name)
            shutil.move(m_file + "/" + file_name, directory + "/" + file_name)  
    removeEmptyFolders(directory)