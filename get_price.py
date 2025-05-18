import requests
import pandas as pd
import os
from datetime import datetime, timedelta

def get_price_data(symbol, interval, limit=100):
    try:
        # Configuration Binance
        endpoint = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol.replace("/", "").upper(),
            "interval": interval,
            "limit": limit
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Conversion en DataFrame
        df = pd.DataFrame(data, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        
        # Conversion des types
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, axis=1)
        
        # Conversion des timestamps
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        
        return df[['open_time', 'open', 'high', 'low', 'close', 'volume']]

    except Exception as e:
        print(f"Erreur lors de la récupération des prix : {str(e)}")
        return None
