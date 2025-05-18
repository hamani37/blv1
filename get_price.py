import requests
import pandas as pd

def get_price_data(symbol, interval):
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": 100
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame(response.json(), columns=cols)[cols]
        df = df.apply(pd.to_numeric, errors='coerce')
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df

    except Exception as e:
        print(f"Erreur récupération prix: {str(e)}")
        return pd.DataFrame()
