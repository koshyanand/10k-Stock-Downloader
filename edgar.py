from bs4 import BeautifulSoup
import csv
import requests 
import pandas

URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&output=xml&CIK="

def load_csv(path, delimiter):
    df = pd.read_csv(path, sep=delimiter  , engine='python')
    return df

russel_1000 = load_csv("russel_1000.csv", "|")

with open('russel_1000.csv', 'w', newline='') as csvfile:
    tick_writer = csv.writer(csvfile, delimiter='||',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for ticker in russel_1000["Ticker"]:
        r = requests.get(URL + ticker) 

        tutorial_soup = BeautifulSoup(r.content, 'lxml')
        name = tutorial_soup.find("name").get_text()
        sic = tutorial_soup.find("sic").get_text()
        cik = tutorial_soup.find("cik").get_text()