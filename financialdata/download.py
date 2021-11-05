import os

import pandas as pd
import pandas_ta as ta
import yfinance as yf

dir_path = os.path.dirname(os.path.realpath(__file__))


def download_ticker(ticker_name):
    """Download the ticker data from the web."""
    return yf.download(ticker_name, period="5y", interval="1d", auto_adjust=True)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add technical indicators to the dataframe."""
    df.ta.strategy(ta.AllStrategy)
    return df


def save_file(df: pd.DataFrame, ticker_name: str) -> str:
    """Save the dataframe to a csv file."""
    # df.to_csv(os.path.join(dir_path, "../output", f"{ticker_name}.csv.gz"), compression='gzip')
    fname = os.path.join(dir_path, "../output", f"{ticker_name}.parquet")
    df.to_parquet(
        fname,
    )

    return df


def process_tickers(*ticker_names: list) -> list:
    """Download the ticker data from the web."""

    df_list = []
    for ticker_name in ticker_names:
        print("Processing ", ticker_name)
        df = download_ticker(ticker_name)
        df = add_indicators(df)
        df_list.append(save_file(df, ticker_name))
    return df_list


if __name__ == "__main__":
    from yahoo_fin import stock_info as si

    tickers = si.tickers_sp500()
    files = process_tickers(*tickers)
