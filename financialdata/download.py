import pandas_ta as ta


def download_ticker(ticker_name):
    """Download the ticker data from the web."""

    import yfinance as yf

    df = yf.download(ticker_name, period="5y", interval="1d", auto_adjust=True)
    df.ta.strategy(ta.AllStrategy)
    return df


if __name__ == "__main__":
    df = download_ticker("TSLA")
    print(df.columns)
