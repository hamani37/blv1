from colorama import Fore, Style, init

init(autoreset=True)

def log_color(message):
    for line in message.splitlines():
        if "Erreur" in line or "❌" in line:
            print(Fore.RED + line)
        elif "🧠" in line:
            print(Fore.CYAN + line)
        elif "✅" in line:
            print(Fore.GREEN + line)
        elif "📈" in line:
            print(Fore.YELLOW + line)
        else:
            print(Style.RESET_ALL + line)
