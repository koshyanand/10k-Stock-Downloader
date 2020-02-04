import yfinance as yf



def get_stock(ticker):

    msft = yf.Ticker(ticker)
    print(msft) 