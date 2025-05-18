import pandas as pd
import numpy as np
from ta.trend import MACD
from ta.momentum import RSI
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
from ta.volatility import AverageTrueRange
from ta.trend import EMAIndicator, SMAIndicator
from ta.trend import VortexIndicator
from ta.volume import MFIIndicator

def supertrend(df, period=10, multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = df['high'].rolling(window=period).max() - df['low'].rolling(window=period).min()
    df['atr'] = df['atr'].rolling(window=period).mean()

    upperband = hl2 + (multiplier * df['atr'])
    lowerband = hl2 - (multiplier * df['atr'])

    supertrend = [True] * len(df)
    for i in range(1, len(df)):
        if df['close'][i] > upperband[i - 1]:
            supertrend[i] = True
        elif df['close'][i] < lowerband[i - 1]:
            supertrend[i] = False
        else:
            supertrend[i] = supertrend[i - 1]
            if supertrend[i] and lowerband[i] < lowerband[i - 1]:
                lowerband[i] = lowerband[i - 1]
            if not supertrend[i] and upperband[i] > upperband[i - 1]:
                upperband[i] = upperband[i - 1]

    final_band = []
    for i in range(len(df)):
        final_band.append(lowerband[i] if supertrend[i] else upperband[i])

    df['Supertrend'] = final_band
    df['Direction'] = np.where(supertrend, 1, -1)
    return df[['Supertrend', 'Direction']]

def get_indicators(df: pd.DataFrame) -> dict:
    indicators = {}

    # RSI
    rsi = RSI(close=df['close'], window=14).rsi()
    indicators['RSI'] = rsi.iloc[-1]

    # MACD
    macd = MACD(close=df['close'])
    indicators['MACD'] = macd.macd().iloc[-1]
    indicators['MACD_signal'] = macd.macd_signal().iloc[-1]

    # Bollinger Bands
    bollinger = BollingerBands(close=df['close'], window=20, window_dev=2)
    indicators['Bollinger_upper'] = bollinger.bollinger_hband().iloc[-1]
    indicators['Bollinger_lower'] = bollinger.bollinger_lband().iloc[-1]

    # OBV
    obv = OnBalanceVolumeIndicator(close=df['close'], volume=df['volume'])
    indicators['OBV'] = obv.on_balance_volume().iloc[-1]

    # ATR
    atr = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'])
    indicators['ATR'] = atr.average_true_range().iloc[-1]

    # VWAP (approximé)
    vwap = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
    indicators['VWAP'] = vwap.iloc[-1]

    # EMA / SMA
    ema = EMAIndicator(close=df['close'], window=20).ema_indicator()
    sma = SMAIndicator(close=df['close'], window=20).sma_indicator()
    indicators['EMA'] = ema.iloc[-1]
    indicators['SMA'] = sma.iloc[-1]

    # MFI
    mfi = MFIIndicator(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'])
    indicators['MFI'] = mfi.money_flow_index().iloc[-1]

    # Vortex
    vortex = VortexIndicator(high=df['high'], low=df['low'], close=df['close'])
    indicators['Vortex_pos'] = vortex.vortex_indicator_pos().iloc[-1]
    indicators['Vortex_neg'] = vortex.vortex_indicator_neg().iloc[-1]

    # Supertrend perso
    super_df = supertrend(df.copy())
    indicators['Supertrend'] = super_df['Supertrend'].iloc[-1]
    indicators['Supertrend_dir'] = super_df['Direction'].iloc[-1]

    return indicators
