import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

class SignalAnalyzer:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.trained = False

    def train(self, data):
        X = list(data['features'])
        y = data['label']
        self.model.fit(X, y)
        self.trained = True

    def predict(self, features):
        if not self.trained:
            return "non_traite"
        return self.model.predict([features])[0]

    def save(self, path="model.pkl"):
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def load(self, path="model.pkl"):
        with open(path, "rb") as f:
            self.model = pickle.load(f)
            self.trained = True
