import websocket
import json
import pandas as pd
from threading import Thread
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeData:
    def __init__(self, symbol='SOL', quote='USD'):
        self.api_key = os.getenv("CRYPTOCOMPARE_API_KEY")
        self.symbol = symbol
        self.quote = quote
        self.df = pd.DataFrame(columns=['timestamp', 'price', 'volume'])
        self.ws = None
        self.active = True
        self.last_log_time = time.time()
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp(
            f"wss://streamer.cryptocompare.com/v2?api_key={self.api_key}",
            on_open=self._on_open,
            on_message=self._handle_message,
            on_error=self._handle_error,
            on_close=self._handle_close
        )
        Thread(target=self.ws.run_forever).start()

    def _on_open(self, ws):
        logger.info("🔌 Connecté au flux temps réel")
        self.subscribe()

    def subscribe(self):
        subscription_message = {
            'action': 'SubAdd',
            'subs': [f'5~CCCAGG~{self.symbol}~{self.quote}']
        }
        logger.debug(f"Subscription message: {subscription_message}")
        self.ws.send(json.dumps(subscription_message))

    def _handle_message(self, ws, message):
        try:
            data = json.loads(message)
            logger.debug(f"Message reçu: {data}")
            if 'TYPE' in data and data['TYPE'] == '5':
                if all(key in data for key in ['PRICE', 'VOLUME24HOUR', 'LASTUPDATE']):
                    timestamp = pd.to_datetime(data['LASTUPDATE'], unit='s')
                    new_data = pd.DataFrame([{
                        'timestamp': timestamp,
                        'price': data['PRICE'],
                        'volume': data['VOLUME24HOUR']
                    }])
                    self.df = pd.concat([self.df, new_data]).tail(1000)

                    # Log only every 10 updates
                    current_time = time.time()
                    if current_time - self.last_log_time > 10:  # Log every 10 seconds
                        logger.info(f"Données mises à jour: {self.df.iloc[-1].to_dict()}")
                        self.last_log_time = current_time
                else:
                    missing_keys = [key for key in ['PRICE', 'VOLUME24HOUR', 'LASTUPDATE'] if key not in data]
                    logger.error(f"Clés manquantes dans les données reçues: {missing_keys}")
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
        if not self.df.empty:
            return self.df.iloc[-1].to_dict()
        else:
            logger.error("Aucune donnée disponible")
            return None

    def get_variation(self, period=60):
        if len(self.df) > period:
            return ((self.df['price'].iloc[-1] - self.df['price'].iloc[-period])
                   / self.df['price'].iloc[-period] * 100)
        return 0.0
