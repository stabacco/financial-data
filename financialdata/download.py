import os

import pandas_ta as ta

dir_path = os.path.dirname(os.path.realpath(__file__))


def download_ticker(ticker_name):
    """Download the ticker data from the web."""

    import yfinance as yf

    df = yf.download(ticker_name, period="5y", interval="1d", auto_adjust=True)
    df.ta.strategy(ta.AllStrategy)
    df.to_csv(os.path.join(dir_path, "../output", f"{ticker_name}.csv"))
    return df


if __name__ == "__main__":
    df = download_ticker("TSLA")
    print(df.columns)
