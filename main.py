import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Server'))

from Server.app import run_flask, get_local_ip
from Console.console import Console
from Makcu.makcu import Makcu
from Recoil.recoil import Recoil
from Config.config import Config

import threading
import time
import sys
import os
from colorama import Fore, Style

def main():
    Console.clear()
    Console.log("INFO", "Looking for Makcu")

    if Makcu.Connect():
        Console.log("INFO", "Makcu has been found")
        
        Console.log("INFO", "Starting button listener")
        Makcu.StartButtonListener()
        Console.log("INFO", "Button listener has been started")

        Console.log("INFO", "Starting Flask web server")
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        Console.log("INFO", "Flask server has started")

        time.sleep(2)
        Console.clear()

        local_ip = get_local_ip()

        print(f"""{Fore.RED}
            ____                         __  __      _                            __
           / / /___ _____ ___  ____ _   / / / /___  (_)   _____  ______________ _/ /
          / / / __ `/ __ `__ \/ __ `/  / / / / __ \/ / | / / _ \/ ___/ ___/ __ `/ / 
         / / / /_/ / / / / / / /_/ /  / /_/ / / / / /| |/ /  __/ /  (__  ) /_/ / /  
        /_/_/\__,_/_/ /_/ /_/\__,_/   \____/_/ /_/_/ |___/\___/_/  /____/\__,_/_/   
        {Style.RESET_ALL}""")
        print(f"[{Fore.RED}+{Style.RESET_ALL}] {Fore.RED}Local:   {Style.RESET_ALL}http://127.0.0.1:5000")
        print(f"[{Fore.RED}+{Style.RESET_ALL}] {Fore.RED}Network: {Style.RESET_ALL}http://{local_ip}:5000")

        Config.load_saved_scripts()
        try:
            while True:
                Recoil.loop()
                time.sleep(0.001) 
        except KeyboardInterrupt:
            Makcu.Disconnect()

if __name__ == "__main__":
    main()
