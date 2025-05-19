import websocket
import json
import pandas as pd
from threading import Thread
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RealTimeData:
    def __init__(self, symbol='solusdt'):
        self.symbol = symbol
        self.df = pd.DataFrame(columns=['timestamp', 'price', 'volume'])
        self.ws = None
        self.active = True
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp(
            f"wss://stream.binance.com:9443/ws/{self.symbol}@trade",
            on_open=lambda ws: logger.info("🔌 Connecté au flux temps réel"),
            on_message=self._handle_message,
            on_error=self._handle_error,
            on_close=self._handle_close
        )
        Thread(target=self.ws.run_forever).start()

    def _handle_message(self, ws, message):
        try:
            trade = json.loads(message)
            new_data = pd.DataFrame([{
                'timestamp': pd.to_datetime(trade['T'], unit='ms'),
                'price': float(trade['p']),
                'volume': float(trade['q'])
            }])
            self.df = pd.concat([self.df, new_data]).tail(1000)
        except Exception as e:
            logger.error(f"Erreur traitement données: {str(e)}")

    def _handle_error(self, ws, error):
        logger.error(f"🚨 Erreur WebSocket: {str(error)}")
        self._reconnect()

    def _handle_close(self, ws, *args):
        logger.info("🔌 Déconnexion du WebSocket")
        self._reconnect()

    def _reconnect(self):
        if self.active:
            logger.info("🔄 Reconnexion dans 5s...")
            time.sleep(5)
            self.connect()

    def get_recent_data(self):
        return self.df.iloc[-1].to_dict() if not self.df.empty else None

    def get_variation(self, period=60):
        if len(self.df) > period:
            return ((self.df['price'].iloc[-1] - self.df['price'].iloc[-period])
                   / self.df['price'].iloc[-period] * 100)
        return 0.0
