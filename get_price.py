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
        
        # Colonnes complètes de la réponse Binance
        columns = [
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ]
        
        # Création du DataFrame avec toutes les colonnes
        df = pd.DataFrame(response.json(), columns=columns)
        
        # Sélection des colonnes utiles
        keep_columns = ['open_time', 'open', 'high', 'low', 'close', 'volume']
        df = df[keep_columns]
        
        # Conversion des types
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Conversion du timestamp
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        
        return df

    except Exception as e:
        print(f"Erreur récupération prix: {str(e)}")
        return pd.DataFrame()
