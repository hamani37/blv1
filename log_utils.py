from colorama import Fore, Style, init
init()

def log_message(msg):
    print(Fore.CYAN + msg + Style.RESET_ALL)

