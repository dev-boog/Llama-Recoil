import json
import os
import random
from Recoil.recoil import Recoil

class Config:
    saved_scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SavedScripts")
    saved_scripts = [{"name": "", "step_count": 0, "values": []}]

    @staticmethod
    def get_script_by_name(name):
        for script in Config.saved_scripts:
            if script["name"] == name:
                return script
        return None

    @staticmethod
    def create_new_script_cfg(name, delay = 100, steps = [{"x":0, "y":10}]):
        if not os.path.exists(Config.saved_scripts_dir):
            os.makedirs(Config.saved_scripts_dir)
        
        script_data = {
            "script_name": name,
            "script_delay": delay,
            "script_steps": steps
        }
        
        filepath = os.path.join(Config.saved_scripts_dir, f"{name}.json")
        with open(filepath, 'w') as f:
            json.dump(script_data, f, indent=4)

        Config.load_saved_scripts()

    @staticmethod
    def update_script(name, delay, steps):
        if not os.path.exists(Config.saved_scripts_dir):
            os.makedirs(Config.saved_scripts_dir)
        
        script_data = {
            "script_name": name,
            "script_delay": delay,
            "script_steps": steps
        }
        
        filepath = os.path.join(Config.saved_scripts_dir, f"{name}.json")
        
        try:
            with open(filepath, 'w') as f:
                json.dump(script_data, f, indent=4)
            Config.load_saved_scripts()
            return True
        except Exception as e:
            return False

    @staticmethod
    def delete_script(name):
        if not os.path.exists(Config.saved_scripts_dir):
            return False
        
        filepath = os.path.join(Config.saved_scripts_dir, f"{name}.json")
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                Config.load_saved_scripts()
                return True
            except Exception as e:
                return False
        return False

    @staticmethod
    def load_saved_scripts():
        Config.saved_scripts = []
        if not os.path.exists(Config.saved_scripts_dir):
            os.makedirs(Config.saved_scripts_dir)

        for filename in os.listdir(Config.saved_scripts_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(Config.saved_scripts_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        name = data.get("script_name", filename)
                        delay = data.get("script_delay", 1)
                        steps = data.get("script_steps", [])
                        Config.saved_scripts.append({
                            "name": name,
                            "step_count": len(steps),
                            "delay": delay,
                            "values": steps
                        })
                except Exception as e:
                    print(f"Error loading script {filename}: {str(e)}")
        
        # Set a random script to Recoil if any scripts were loaded
        if Config.saved_scripts:
            random_script = random.choice(Config.saved_scripts)
            Recoil.advanced_mode_script = random_script["name"]

        
        