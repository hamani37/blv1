import os
import json
import pickle
import random
import time
from datetime import datetime
from threading import Thread
from utils.logbook import log_signal
from sklearn.ensemble import RandomForestClassifier

class TradingIA:
    def __init__(self):
        self.data_file = "data/live_data.json"
        self.state_file = "data/model_state.pkl"
        self.price_history = []
        self.current_signal = None
        self.model = RandomForestClassifier()
        self.is_trained = False
        self.X = []
        self.y = []
        self.load_state()
        Thread(target=self.track_price).start()

    def load_state(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.state_file):
            with open(self.state_file, "rb") as f:
                state = pickle.load(f)
                self.X = state["X"]
                self.y = state["y"]
                self.model = state["model"]
                self.is_trained = state["is_trained"]
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump({}, f)

    def save_state(self):
        state = {
            "X": self.X,
            "y": self.y,
            "model": self.model,
            "is_trained": self.is_trained
        }
        with open(self.state_file, "wb") as f:
            pickle.dump(state, f)

    def get_live_price(self):
        try:
            import requests
            res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
            return res.json()["solana"]["usd"]
        except:
            return None

    def track_price(self):
        while True:
            price = self.get_live_price()
            if price:
                timestamp = datetime.utcnow().isoformat()
                self.price_history.append((timestamp, price))
                self.save_live_data()
            time.sleep(1)

    def save_live_data(self):
        with open(self.data_file, "w") as f:
            json.dump({"price_history": self.price_history[-3600:]}, f)

    def train_model(self):
        if len(self.X) >= 50:
            self.model.fit(self.X, self.y)
            self.is_trained = True
            self.save_state()

    def process_signal(self, signal_type):
        current_price = self.get_live_price()
        features = self.extract_features(current_price)
        log_signal(signal_type, current_price, features)

        if not self.is_trained:
            label = 1 if random.random() > 0.5 else 0
            self.X.append(features)
            self.y.append(label)
            print(f"📚 Apprentissage en cours : {len(self.X)}/50")
            self.train_model()
            return "Phase d'apprentissage"
        else:
            prediction = self.model.predict([features])[0]
            judgement = self.explain_signal(signal_type, features, prediction)
            return judgement

    def extract_features(self, price):
        return [
            round(random.uniform(20, 80), 2),  # RSI
            round(random.uniform(-1, 1), 2),   # MACD
            round(random.uniform(0.5, 1.5), 2),# Bollinger
            round(random.uniform(1000, 10000), 2)  # OBV
        ]

    def explain_signal(self, signal_type, features, prediction):
        rsi, macd, boll, obv = features
        if prediction:
            return f"📊 Signal {signal_type.upper()} jugé BON ✅ – RSI: {rsi}, MACD: {macd}, Boll: {boll}, OBV: {obv} – Raisonnement IA : \"Y'a du potentiel ici, ça sent le pognon 💸 !\""
        else:
            return f"📊 Signal {signal_type.upper()} jugé MAUVAIS ❌ – RSI: {rsi}, MACD: {macd}, Boll: {boll}, OBV: {obv} – Raisonnement IA : \"Laisse tomber, c'est de la daube ce signal... 💩\""
