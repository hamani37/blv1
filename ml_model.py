def process_signal(signal, price):
    signal_type = signal["type"]
    message = ""
    if signal_type == "long":
        message = "Le signal dit LONG. RSI ? Bon. MACD ? Positif. Volume ? Pas mal. On y va à l’achat comme un ouf !"
    elif signal_type == "short":
        message = "Signal SHORT reçu. RSI ? Trop haut. MACD ? Pique du nez. Volume ? Baisse. On short comme un chacal !"
    else:
        message = "Signal non reconnu. L’IA panique. Elle préfère rien faire et se gratter le nez."
    return message
