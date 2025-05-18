import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator

def get_indicators(df):
    try:
        if df.empty or len(df) < 20:
            return {}

        # RSI 14
        rsi = RSIIndicator(df['close'], window=14)
        df['rsi'] = rsi.rsi()

        # MACD
        macd = MACD(df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()

        # Bollinger Bands
        bb = BollingerBands(df['close'], window=20)
        df['bollinger_high'] = bb.bollinger_hband()
        df['bollinger_low'] = bb.bollinger_lband()

        # OBV
        obv = OnBalanceVolumeIndicator(df['close'], df['volume'])
        df['obv'] = obv.on_balance_volume()

        return {
            'rsi': round(df['rsi'].iloc[-1], 2),
            'macd': round(df['macd'].iloc[-1], 5),
            'macd_signal': round(df['macd_signal'].iloc[-1], 5),
            'bollinger_high': round(df['bollinger_high'].iloc[-1], 5),
            'bollinger_low': round(df['bollinger_low'].iloc[-1], 5),
            'obv': round(df['obv'].iloc[-1], 2)
        }

    except Exception as e:
        print(f"Erreur indicateurs: {str(e)}")
        return {}
