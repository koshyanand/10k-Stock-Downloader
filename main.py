import csv 
import pandas as pd

def load_csv(path, delimiter):
    df = pd.read_csv(path, sep=delimiter  , engine='python')
    return df

cik_ticker = load_csv("cik_ticker.csv", "|")
russel_1000 = load_csv("russel_1000.csv", "|")

i, j, k = 0, 0, 0
for tick in russel_1000["Ticker"]:
    df = cik_ticker.loc[(cik_ticker["Ticker"] == tick)]

    # df = cik_ticker.loc[(cik_ticker["Ticker"] == tick) & ((cik_ticker["Exchange"] == "NYSE") | (cik_ticker["Exchange"] == "NYSE MKT") | (cik_ticker["Exchange"] == "NYSE ARCA"))]
    if len(df) > 1:
        # print(df)
        i += 1
    elif len(df) == 0:
        # print("Zero")
        print(tick)
        j += 1
    else:
        # print("Success")
        k += 1

print(i, j, k)

