import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, CCIIndicator
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
from ta.trend import SMAIndicator, EMAIndicator
import json

def get_indicators(df):
    if df is None or df.empty:
        return {}

    df = df.copy()

    # RSI
    rsi = RSIIndicator(close=df['close'], window=14)
    df['rsi'] = rsi.rsi()

    # MACD
    macd = MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    # Bollinger Bands
    boll = BollingerBands(close=df['close'], window=20, window_dev=2)
    df['boll_upper'] = boll.bollinger_hband()
    df['boll_lower'] = boll.bollinger_lband()

    # OBV
    obv = OnBalanceVolumeIndicator(close=df['close'], volume=df['volume'])
    df['obv'] = obv.on_balance_volume()

    # SMA 50
    sma50 = SMAIndicator(close=df['close'], window=50)
    df['sma50'] = sma50.sma_indicator()

    # EMA 20
    ema20 = EMAIndicator(close=df['close'], window=20)
    df['ema20'] = ema20.ema_indicator()

    # CCI
    cci = CCIIndicator(high=df['high'], low=df['low'], close=df['close'], window=20)
    df['cci'] = cci.cci()

    # Variation entre les deux derniers signaux
    if len(df) >= 2:
        df['variation_pct'] = (df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2] * 100
    else:
        df['variation_pct'] = 0

    # Résumé final
    latest = df.iloc[-1]
    indicators = {
        'rsi': round(latest['rsi'], 2),
        'macd': round(latest['macd'], 5),
        'macd_signal': round(latest['macd_signal'], 5),
        'boll_upper': round(latest['boll_upper'], 5),
        'boll_lower': round(latest['boll_lower'], 5),
        'obv': round(latest['obv'], 2),
        'sma50': round(latest['sma50'], 5),
        'ema20': round(latest['ema20'], 5),
        'cci': round(latest['cci'], 2),
        'variation_pct': round(latest['variation_pct'], 2)
    }

    return indicators

def is_signal_valid(signal_type, indicators):
    variation = indicators.get('variation_pct', 0)
    
    if signal_type == "LONG" and variation >= 0.5:
        return True
    elif signal_type == "SHORT" and variation <= -0.5:
        return True
    else:
        return False
