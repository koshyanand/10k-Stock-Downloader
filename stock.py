import yfinance as yf
from util import load_csv
import datetime
import os, csv
DATE_FORMAT  = '%Y%m%d'

def get_stock(ticker, day):
    day_str = day.strftime('%Y-%m-%d')
    data = yf.download(ticker, start=day_str, end=day_str)
    i = 0
    while (len(data) == 0):
        if i > 10:
            return None, None
        day = add_days_to_date(day, 2)
        day_str = day.strftime('%Y-%m-%d')
        data = yf.download(ticker, start=day_str, end=day_str)
        i += 1
    return day, data


def get_date_to_search(date_string):
    date_time_obj = datetime.datetime.strptime(date_string, DATE_FORMAT)
    # print(date_time_obj.isoformat())

    future_date = (date_time_obj + datetime.timedelta(6*365/12))
    week_no = future_date.weekday()

    if week_no > 4:
        future_date = future_date + datetime.timedelta(days=3)
    return future_date

def add_days_to_date(date, days):
    date = date + datetime.timedelta(days = days)
    return date




df = load_csv("data/sec_filing_date.csv", "|")

stock_data = []

with open("data/stock_data.csv", 'a', newline='') as file:
    writer = csv.writer(file, delimiter="|")
    # writer.writerows(stock_data)

    for row in df.itertuples():
        if row.Year != 18:
            continue
        ticker = row.Ticker
        name = row.Name
        print(ticker)

        filing_date = datetime.datetime.strptime(str(row.FilingDate), DATE_FORMAT)
        final_filing_date, data = get_stock(ticker, filing_date)
        if final_filing_date == None:
            print("Error :" + ticker)
            continue
        filing_day_stock = round(data["Open"][0], 2)
        # print("Final : " + str(filing_day_stock))
        # print(data)

        future_date = get_date_to_search(str(row.FilingDate))
        final_future_date, data = get_stock(ticker, future_date)
        future_day_stock = round(data["Open"][0], 2)
        # print(data)
        # print("Future : " + str(future_day_stock))
        stock = [ticker, name, filing_date.strftime('%Y-%m-%d'), final_filing_date.strftime('%Y-%m-%d'), filing_day_stock, final_future_date.strftime('%Y-%m-%d'), future_day_stock, row.Path]
        writer.writerow(stock)
        # stock_data.append(stock)
    # break





