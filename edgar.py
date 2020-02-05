from bs4 import BeautifulSoup
import csv
import requests 
import pandas as pd

URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&output=xml&CIK="

def load_csv(path, delimiter):
    df = pd.read_csv(path, sep=delimiter  , engine='python')
    return df

russel_1000 = load_csv("russel_1000.csv", "|")
# print(russel_1000)
error = []
with open('r_1000.csv', 'w', newline='') as csvfile:
    tick_writer = csv.writer(csvfile, delimiter='|')

    for i, row in russel_1000.iterrows():
        # print(ticker)
        ticker = row[1].replace(".", "")
        name = row[0]
        
        r = requests.get(URL + ticker)

        tutorial_soup = BeautifulSoup(r.content, 'lxml')

        if tutorial_soup.find("name") == None:
            print(ticker + " : error")
            error.append(ticker)
            continue
        # name = tutorial_soup.find("name").get_text()
        if tutorial_soup.find("sic") == None:
            sic = None
        else:
            sic = tutorial_soup.find("sic").get_text()

        cik = tutorial_soup.find("cik").get_text()
        print([ticker, name, cik, sic])
        tick_writer.writerow([ticker, name, cik, sic])

print("Errors : " + error)
