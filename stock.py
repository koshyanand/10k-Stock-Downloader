import yfinance as yf
from util import load_csv
import datetime

DATE_FORMAT  = '%Y%m%d'
def get_stock(ticker, day):
    data = yf.download(ticker, start="2017-01-01", end="2017-01-01")
    print(data)


date_time_obj = datetime.datetime.strptime("20181105", DATE_FORMAT)
print(date_time_obj.isoformat())

future_date = (date_time_obj + datetime.timedelta(6*365/12))
week_no = future_date.weekday()
if week_no > 4:
    future_date = future_date + datetime.timedelta(days=3)

# def add
print((date_time_obj + datetime.timedelta(6*365/12)).isoformat())


# df = load_csv("data/sec_filing_date.csv", "|")

# for row in df.iterrows():
#     date = row["FilingDate"]
#     date_time_obj = datetime.datetime.strptime(date_time_str, DATE_FORMAT)

# get_stock(["MMM", "AMZN"])