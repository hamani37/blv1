import requests
import pandas as pd
import numpy as np
from ta.trend import MACD, CCIIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
from ta.trend import EMAIndicator
from ta.trend import SuperTrend

def get_binance_data(pair="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])

    df['close'] = pd.to_numeric(df['close'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['volume'] = pd.to_numeric(df['volume'])

    return df

def get_indicators(pair="BTCUSDT"):
    df = get_binance_data(pair)

    indicators = {}

    df['rsi'] = RSIIndicator(close=df['close']).rsi()
    df['macd'] = MACD(close=df['close']).macd_diff()
    df['obv'] = OnBalanceVolumeIndicator(close=df['close'], volume=df['volume']).on_balance_volume()
    bb = BollingerBands(close=df['close'])
    df['bollinger_width'] = bb.bollinger_wband()
    df['ema20'] = EMAIndicator(close=df['close'], window=20).ema_indicator()

    indicators['RSI'] = round(df['rsi'].iloc[-1], 2)
    indicators['MACD'] = round(df['macd'].iloc[-1], 4)
    indicators['OBV'] = round(df['obv'].iloc[-1], 2)
    indicators['Bollinger_Width'] = round(df['bollinger_width'].iloc[-1], 4)
    indicators['EMA20'] = round(df['ema20'].iloc[-1], 2)

    return indicators
