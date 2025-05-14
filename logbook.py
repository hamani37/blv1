from colorama import Fore, Style

def log_signal_info(signal_type, indicators):
    print(f"{Fore.GREEN if signal_type == 'long' else Fore.RED}📈 Signal: {signal_type.upper()} | "
          f"Prix: {indicators['last']} | RSI: {indicators['rsi']} | "
          f"MACD: {indicators['macd']} | Boll: {indicators['boll']} | OBV: {indicators['obv']}"
          f"{Style.RESET_ALL}")
    print(f"🟡 Variation max : {indicators['high']} | Variation min : {indicators['low']}")
    print("Phase d'apprentissage")
