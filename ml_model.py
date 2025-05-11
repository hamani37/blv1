# ml_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import pickle
import datetime
import json

# Initialisation du modèle IA
model = RandomForestClassifier(n_estimators=100, random_state=42)
scaler = StandardScaler()

# Historique des signaux (mémoire)
SIGNAL_HISTORY_FILE = "signal_history.json"
MODEL_FILE = "trained_model.pkl"

def load_signal_history():
    if os.path.exists(SIGNAL_HISTORY_FILE):
        with open(SIGNAL_HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_signal_history(history):
    with open(SIGNAL_HISTORY_FILE, "w") as f:
        json.dump(history, f)

def add_signal_to_history(signal_data):
    history = load_signal_history()
    history.append(signal_data)
    save_signal_history(history)

def prepare_training_data():
    history = load_signal_history()
    if len(history) < 10:
        return None, None

    df = pd.DataFrame(history)

    # On suppose que la colonne 'valid' est le label, les autres sont les features
    if 'valid' not in df.columns:
        return None, None

    X = df.drop(columns=['valid', 'type', 'timestamp'])
    y = df['valid']

    X_scaled = scaler.fit_transform(X)
    return X_scaled, y

def train_model():
    X, y = prepare_training_data()
    if X is None or y is None:
        return None
    model.fit(X, y)
    with open(MODEL_FILE, "wb") as f:
        pickle.dump((model, scaler), f)

def load_model():
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, "rb") as f:
            return pickle.load(f)
    return None, None

def evaluate_signal(features):
    # Charger le modèle entraîné
    trained_model, trained_scaler = load_model()
    if not trained_model or not trained_scaler:
        return False

    df = pd.DataFrame([features])
    df_scaled = trained_scaler.transform(df)
    prediction = trained_model.predict(df_scaled)

    return prediction[0] == 1
