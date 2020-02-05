import yfinance as yf


def get_stock(ticker):
    data = yf.download(ticker, start="2017-01-01", end="2017-01-01")

    # msft = yf.Ticker(ticker)
    # print(msft.info)
    # print(msft.history(period="max"))
    print(data)

get_stock(["MMM", "AMZN"])