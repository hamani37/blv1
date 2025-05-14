from colorama import Fore, Style

def enregistrer_log(signal, info, interpretation, phase):
    direction = signal["type"].upper()
    prix = info["price"]
    print(f"{Fore.CYAN}📈 Signal: {direction} | Prix: {prix:.2f} | RSI: {info['rsi']} | MACD: {info['macd']} | Boll: {info['bollinger']} | OBV: {info['obv']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{phase}{Style.RESET_ALL}")
    print(f"{Fore.GREEN if '✅' in interpretation else Fore.RED}{interpretation}{Style.RESET_ALL}")
