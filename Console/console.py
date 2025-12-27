from colorama import init, Fore, Style
from datetime import datetime
import os

init(autoreset=True)


class Console:
    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def log(level, message):
        current_time = datetime.now().strftime("%H:%M:%S")

        color = {
            "INFO": Fore.GREEN,
            "WARN": Fore.YELLOW,
            "ERROR": Fore.RED,
            "DEBUG": Fore.CYAN
        }.get(level.upper(), Fore.WHITE)

        print(f"{Fore.BLACK + Style.BRIGHT}{current_time}{Style.RESET_ALL} {color}{level}{Style.RESET_ALL} {message}")
