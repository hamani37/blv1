import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_signal_with_ai(signal_data, live_data):
    prompt = f"""
Tu es une IA de trading sérieuse.
Voici le signal TradingView reçu : {signal_data}
Voici les données live actuelles : {live_data}

Analyse-les avec les indicateurs (RSI, MACD, Bollinger, OBV, VWAP, SuperTrend, ATR...) et décide :
1. Si c'est un bon moment pour entrer.
2. Si c’est un signal pour un trade LONG, SHORT ou à ignorer.
3. Explique ta décision clairement avec les indicateurs.

Réponds uniquement sous cette forme :
Decision: [LONG/SHORT/IGNORE]
Explication: [ton analyse sérieuse]
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message["content"]
    lines = content.split("\n")
    decision_line = next((line for line in lines if line.startswith("Decision:")), None)
    explanation_line = next((line for line in lines if line.startswith("Explication:")), None)

    decision = decision_line.split("Decision:")[1].strip() if decision_line else "IGNORE"
    explanation = explanation_line.split("Explication:")[1].strip() if explanation_line else "Pas d'explication."

    return decision, explanation
