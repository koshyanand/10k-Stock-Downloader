from bs4 import BeautifulSoup
import csv
import requests 
import pandas as pd
from SECEdgar.filings import Filing, FilingType
import os, sys
from util import load_csv, load_txt_file, remove_extra_data
import time

FILING_SEARCH_START = "FILED AS OF DATE:"
FILING_SEARCH_END = "DATE AS OF CHANGE:"

URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&output=xml&CIK="


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



def add_ticker_info_to_db(path, db_path, ticker, filing_type, name):
    if not os.path.isdir(path):
        return False
    files = os.listdir(path)

    with open(db_path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter="|")
    
        for f in files:
            year = f.split("_")[2]
            year = year.replace(".txt", "")
            file_path = os.path.join(path, f)
            data = load_txt_file(path, f)
            filing_date = data[data.find(FILING_SEARCH_START) + len(FILING_SEARCH_START) : data.find(FILING_SEARCH_END)]
            filing_date = filing_date.strip()
            writer.writerow([ticker, name, filing_type, year, filing_date, file_path])
    return True
# remove_extra_data('data/' + "AAPL" + "/", "10-K", 2018)
error_list = []
def get_10k_from_cik(df, year, db_path):
    for row in df.itertuples():
        ticker = row.Ticker

        try:
            name = row.Name
            print(ticker)
            # print(time.)
            my_filings = Filing(row.CIK, filing_type=FilingType.FILING_10K, count = 2)
            my_filings.save('data/SEC/10-k/' + ticker + "/")
            remove_extra_data('data/SEC/10-k/' + ticker, "10-k")
            e = add_ticker_info_to_db('data/SEC/10-k/' + ticker, db_path, ticker, "1O-k", name)
            if not e:
                error_list.append(ticker)
                print("Error : " + ticker)  
        except:
            error_list.append(ticker)
            print("Error : " + ticker)
        # time.sleep(1)
        # break

df = load_csv("r_1000.csv", "|")
get_10k_from_cik(df, 18, "data/sec_filing_date.csv")
print(error_list)
