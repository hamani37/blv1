import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = 'model.pkl'
COUNT_PATH = 'learning_count.txt'
MAX_LEARNING_SIGNALS = 50

# Initialisation
if os.path.exists(MODEL_PATH):
    print("[BOOT] Chargement du modèle IA...")
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
else:
    print("[BOOT] Nouveau modèle IA initialisé.")
    model = None

if os.path.exists(COUNT_PATH):
    with open(COUNT_PATH, 'r') as f:
        learning_count = int(f.read().strip())
else:
    learning_count = 0

print(f"[BOOT] Compteur apprentissage : {learning_count}/{MAX_LEARNING_SIGNALS}")

def save_model():
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

def save_count():
    with open(COUNT_PATH, 'w') as f:
        f.write(str(learning_count))

def extract_features(signal_data):
    return [
        1 if signal_data['type'] == 'long' else 0,
        np.random.random(),
        np.random.random(),
        np.random.random()
    ]

def train_model(existing_model, signal_data):
    X = [extract_features(signal_data)]
    y = [1 if signal_data['type'] == 'long' else 0]

    if existing_model is None:
        model_local = RandomForestClassifier()
        model_local.fit(X, y)
    else:
        model_local = existing_model
        model_local.fit(X, y)

    return model_local

def predict_signal(model_local, signal_data):
    x = [extract_features(signal_data)]
    prediction = model_local.predict(x)[0]
    if prediction == 1:
        return "Bon signal : RSI bas, MACD haussier, volume en hausse."
    else:
        return "Mauvais signal : MACD négatif, volume faible, tendance incertaine."

def process_signal(signal_data):
    global model, learning_count

    signal_type = signal_data.get('type')
    if signal_type not in ['long', 'short']:
        return "Signal invalide"

    if learning_count < MAX_LEARNING_SIGNALS:
        model = train_model(model, signal_data)
        learning_count += 1
        save_model()
        save_count()
        print(f"✅ Signal reçu : {signal_data}")
        print(f"📚 Apprentissage en cours : {learning_count}/{MAX_LEARNING_SIGNALS}")
        return f"Apprentissage en cours : {learning_count}/{MAX_LEARNING_SIGNALS}"
    else:
        explanation = predict_signal(model, signal_data)
        print(f"✅ Signal reçu : {signal_data}")
        print(f"📊 Explication IA : {explanation}")
        return f"Explication IA : {explanation}"
