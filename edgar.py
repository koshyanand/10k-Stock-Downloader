from bs4 import BeautifulSoup
import csv
import requests 
import pandas as pd
from SECEdgar.filings import Filing, FilingType
import os, sys
import shutil  

URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&output=xml&CIK="

def load_csv(path, delimiter):
    df = pd.read_csv(path, sep=delimiter  , engine='python')
    return df

def get_cik_from_ticker(df):
    errors = []
    output_list = []
    for i, row in df.iterrows():
        ticker = row[1].replace(".", "")
        name = row[0]
        
        r = requests.get(URL + ticker)

        tutorial_soup = BeautifulSoup(r.content, 'lxml')

        if tutorial_soup.find("name") == None:
            print(ticker + " : error")
            errors.append(ticker)
            continue
        # name = tutorial_soup.find("name").get_text()
        if tutorial_soup.find("sic") == None:
            sic = None
        else:
            sic = tutorial_soup.find("sic").get_text()

        cik = tutorial_soup.find("cik").get_text()

        output_list.append((ticker, name, cik, sic))

    return output_list, errors

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
            # print(vals)
            # if int(vals[1]) != year:
            #     os.remove(m_file + "/" + sub_file)
            # else:
            file_name = "sec_10k_" + str(vals[1]) + ".txt"
            os.rename(m_file + "/" + sub_file, m_file + "/" + file_name)
            shutil.move(m_file + "/" + file_name, directory + "/" + file_name)  
    removeEmptyFolders(directory)
                # return


# remove_extra_data('data/' + "AAPL" + "/", "10-K", 2018)
def get_10k_from_cik(cik_ticker_list, year):
    for cik, ticker in cik_ticker_list:
        print(ticker)
        my_filings = Filing(cik, filing_type=FilingType.FILING_10K, count = 2)
        my_filings.save('data/SEC/10-k/' + ticker + "/")
        remove_extra_data('data/SEC/10-k/' + ticker, "10-k")
        # break

get_10k_from_cik([("0000320193", "AAPL")], 18)
