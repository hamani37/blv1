from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os

model_path = "utils/model.pkl"
dataset_path = "utils/signaux.csv"

# Création du fichier si non existant
if not os.path.exists(dataset_path):
    df = pd.DataFrame(columns=["rsi", "macd", "volume", "trend", "label"])
    df.to_csv(dataset_path, index=False)

def train_model():
    df = pd.read_csv(dataset_path)
    if len(df) < 10:
        print("📉 Pas assez de données pour entraîner le modèle.")
        return None

    X = df[["rsi", "macd", "volume", "trend"]]
    y = df["label"]

    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, model_path)
    print("✅ Modèle IA entraîné et sauvegardé.")

def predict(features):
    if not os.path.exists(model_path):
        print("⚠️ Modèle non trouvé. Entraînez-le d'abord.")
        return "skip"

    model = joblib.load(model_path)
    result = model.predict([features])[0]
    return result
