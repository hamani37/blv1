import requests
import logging
import time
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeData:
    def __init__(self, symbol='SOLUSDT'):
        self.symbol = symbol
        self.df = pd.DataFrame(columns=['timestamp', 'price'])
        self.last_log_time = time.time()
        self.get_price()

    def get_price(self):
        try:
            response = requests.get(
                f"https://api.binance.com/api/v3/ticker/price",
                params={"symbol": self.symbol}
            )

            if response.status_code == 200:
                json_response = response.json()
                logger.debug(f"Réponse de l'API: {json_response}")
                price = float(json_response.get('price', None))
                if price is not None:
                    timestamp = pd.Timestamp.now()
                    new_data = pd.DataFrame([{
                        'timestamp': timestamp,
                        'price': price
                    }])
                    self.df = pd.concat([self.df, new_data]).tail(1000)

                    # Log only every 10 updates
                    current_time = time.time()
                    if current_time - self.last_log_time > 10:  # Log every 10 seconds
                        logger.info(f"Données mises à jour: {self.df.iloc[-1].to_dict()}")
                        self.last_log_time = current_time
                else:
                    logger.error("Clé de prix manquante dans les données reçues")
            else:
                logger.error("Erreur lors de la récupération des données: %s %s", response.status_code, response.text)
        except Exception as e:
            logger.error("Exception lors de la récupération des données: %s", str(e))

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

if __name__ == "__main__":
    sol_data = RealTimeData(symbol='SOLUSDT')
    recent_data = sol_data.get_recent_data()
    if recent_data:
        print("Données récentes de SOL en USDT:", recent_data)
