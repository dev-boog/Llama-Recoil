import time
from Makcu.makcu import Makcu


class Recoil:
    enabled = False
    shot_count = 0
    mode = "simple-mode"

    simple_mode_x = 0
    simple_mode_y = 0
    simple_mode_delay = 1
    simple_hipfire = False  

    advanced_mode_script = []
    advanced_mode_delay = 1
    advanced_loop_when_complete = False
    advanced_hipfire = False

    test_mode_active = False
    test_mode_steps = []
    test_mode_delay = 100
    _saved_enabled = False
    _saved_mode = "simple-mode"
    _saved_hipfire = False


    @staticmethod
    def loop():
        # Check button states based on hipfire mode and current mode
        if Recoil.mode == "simple-mode":
            if Recoil.simple_hipfire:
                # Hipfire: Works with LMB only
                button_check = Makcu.GetButtonState("LMB")
            else:
                # Normal: Requires both RMB and LMB
                button_check = Makcu.GetButtonState("RMB") and Makcu.GetButtonState("LMB")
        elif Recoil.mode == "advanced-mode":
            if Recoil.advanced_hipfire:
                # Hipfire: Works with LMB only
                button_check = Makcu.GetButtonState("LMB")
            else:
                # Normal: Requires both RMB and LMB
                button_check = Makcu.GetButtonState("RMB") and Makcu.GetButtonState("LMB")
        else:
            button_check = False
        
        if button_check and Recoil.enabled:
            if Recoil.mode == "simple-mode":
                Makcu.move_mouse_smoothly(Recoil.simple_mode_x, Recoil.simple_mode_y)
                Makcu.precise_sleep(Recoil.simple_mode_delay)
                Recoil.shot_count += 1
            elif Recoil.mode == "advanced-mode":
                if Recoil.test_mode_active and Recoil.test_mode_steps:
                    step_count = len(Recoil.test_mode_steps)
                    if Recoil.shot_count >= step_count:
                        # Pattern complete, stop until buttons released
                        return
                    
                    step = Recoil.test_mode_steps[Recoil.shot_count]
                    x = step.get("x", 0)
                    y = step.get("y", 0)
                    delay = Recoil.test_mode_delay / 1000.0
                    Makcu.move_mouse_smoothly(x, y)
                    Makcu.precise_sleep(delay)
                    Recoil.shot_count += 1
                else:
                    from Config.config import Config
                    loaded_script = Config.get_script_by_name(Recoil.advanced_mode_script)
                    if loaded_script:
                        if Recoil.shot_count >= loaded_script["step_count"]:
                            if Recoil.advanced_loop_when_complete:
                                Recoil.shot_count = 0  # Reset to loop
                            else:
                                # Don't reset, just stop executing until button is released and pressed again
                                return
                        
                        if Recoil.shot_count < loaded_script["step_count"]:
                            step = loaded_script["values"][Recoil.shot_count]
                            x = step.get("x", 0)
                            y = step.get("y", 0)
                            delay = loaded_script.get("delay", 100) / 1000.0
                            Makcu.move_mouse_smoothly(x, y)
                            Makcu.precise_sleep(delay)
                            Recoil.shot_count += 1
        else:
            # Reset shot count when buttons are released
            Recoil.shot_count = 0
        