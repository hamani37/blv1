import json
from colorama import Fore, Style
import os

def log_with_color(signal, price, decision, explanation):
    print(f"{Fore.YELLOW}[SIGNAL]{Style.RESET_ALL} {signal} | {Fore.GREEN}Prix:{price}{Style.RESET_ALL} | "
          f"{Fore.CYAN}Décision IA:{decision}{Style.RESET_ALL} | {Fore.MAGENTA}{explanation}{Style.RESET_ALL}")

def save_signal_data(signal, price, decision, explanation, timestamp):
    entry = {
        "timestamp": timestamp,
        "signal": signal,
        "price": price,
        "decision": decision,
        "explanation": explanation
    }

    if os.path.exists("live_data.json"):
        with open("live_data.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(entry)

    with open("live_data.json", "w") as file:
        json.dump(data, file, indent=4)
