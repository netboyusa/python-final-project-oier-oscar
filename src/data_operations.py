import krakenex
import pandas as pd
import streamlit as st


def download_data(pair, interval):
    try:
        api = krakenex.API()
        data = api.query_public("OHLC", {"pair": pair, "interval": interval})
        df = pd.DataFrame(data["result"][pair], columns=["time", "open", "high", "low", "close", "vwap", "volume", "count"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
        df["date"] = df["time"].apply(lambda x: x.date())
        return df
    except Exception as e:
        st.error(f"Error downloading data: {e}")
        return pd.DataFrame()

def get_available_pairs():
    try:
        api = krakenex.API()
        asset_pairs = api.query_public('AssetPairs')
        pairs = list(asset_pairs['result'].keys())
        return pairs
    except Exception as e:
        st.error(f"Error getting available pairs: {e}")
        return []
