import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

def calculate_indicators(df):
    try:
        # Calcul du RSI
        df['rsi'] = RSIIndicator(df['price'], window=14).rsi()
        
        # Calcul du MACD
        macd = MACD(df['price'])
        df['macd_line'] = macd.macd()
        df['signal_line'] = macd.macd_signal()
        
        return {
            'rsi': round(df['rsi'].iloc[-1], 2),
            'macd_diff': round(df['macd_line'].iloc[-1] - df['signal_line'].iloc[-1], 4),
            'variation_1m': round(df['price'].pct_change(60).iloc[-1] * 100, 2)
        }
    except Exception as e:
        print(f"Erreur calcul indicateurs: {str(e)}")
        return {}
