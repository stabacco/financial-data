import os

import pandas as pd
import pandas_ta as ta
import yfinance as yf
from yahoo_fin import stock_info as si

dir_path = os.path.dirname(os.path.realpath(__file__))


def download_ticker(ticker_name):
    """Download the ticker data from the web."""
    return yf.download(ticker_name, period="5y", interval="1d", auto_adjust=True)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add technical indicators to the dataframe."""
    strategy = ta.Strategy(
        name="Common Price and Volume SMAs",
        description="Common Price SMAs: 10, 20, 50, 200 and Volume SMA: 20.",
        ta=[
            {"kind": "sma", "length": 10},
            {"kind": "sma", "length": 20},
            {"kind": "sma", "length": 50},
            {"kind": "sma", "length": 150},
            {"kind": "sma", "length": 200},
            {"kind": "bbands", "length": 20},
            {"kind": "rsi"},
            {"kind": "stoch"},
            {
                "kind": "kc",
            },
            {"kind": "macd"},
            {"kind": "roc"},
            {"kind": "atr", "length": 14},
            {"kind": "stdev"},
        ],
    )
    df.ta.strategy(strategy)
    return df


def save_file(df: pd.DataFrame, ticker_name: str) -> str:
    """Save the dataframe to a csv file."""
    # df.to_csv(os.path.join(dir_path, "../output",
    # f"{ticker_name}.csv.gz"), compression='gzip')
    fname = os.path.join(dir_path, "../output", f"{ticker_name}.parquet")
    df.to_parquet(
        fname,
    )

    return df


def process_tickers(*ticker_names: str) -> list:
    """Download the ticker data from the web."""

    df_list = []
    for ticker_name in ticker_names:
        try:
            print("Processing ", ticker_name)
            df = download_ticker(ticker_name)
            df = add_indicators(df)
            df_list.append(save_file(df=df, ticker_name=ticker_name))
        except Exception as e:
            print("failed to process: reason {e}".format(e=e))
    return df_list


if __name__ == "__main__":

    tickers = si.tickers_sp500()
    files = process_tickers(*tickers)
