import time
import os
import sys
import io
from makcu import create_controller, MouseButton
import makcu.connection

class Makcu:
    _controller = None
    _button_states = {"LMB": False, "RMB": False}
    _original_handle_button_data = None
    
    @staticmethod
    def _patched_handle_button_data(self, byte_val: int):
        if byte_val == self._last_button_mask:
            return

        changed_bits = byte_val ^ self._last_button_mask

        for bit in range(8):
            if changed_bits & (1 << bit):
                is_pressed = bool(byte_val & (1 << bit))
            
                if is_pressed:
                    self._button_states |= (1 << bit)
                else:
                    self._button_states &= ~(1 << bit)
            
                if self._button_callback and bit < len(self.BUTTON_ENUM_MAP):
                    try:
                        self._button_callback(self.BUTTON_ENUM_MAP[bit], is_pressed)
                    except Exception:
                        pass

        self._last_button_mask = byte_val
    
    @staticmethod
    def Connect():
        try:
            Makcu._original_handle_button_data = makcu.connection.SerialTransport._handle_button_data
            makcu.connection.SerialTransport._handle_button_data = Makcu._patched_handle_button_data
            
            Makcu._controller = create_controller(debug=False, auto_reconnect=True)
            
            def on_button_event(button: MouseButton, pressed: bool):
                if button == MouseButton.LEFT:
                    Makcu._button_states["LMB"] = pressed
                elif button == MouseButton.RIGHT:
                    Makcu._button_states["RMB"] = pressed
            
            Makcu._controller.set_button_callback(on_button_event)
            Makcu._controller.enable_button_monitoring(True)
            
            return True
        except Exception as e:
            if Makcu._original_handle_button_data:
                makcu.connection.SerialTransport._handle_button_data = Makcu._original_handle_button_data
            print(f"Makcu connection error: {str(e)}")
            return False
    
    @staticmethod
    def MoveMouse(x, y):
        if Makcu._controller:
            try:
                Makcu._controller.move(int(x), int(y))
            except Exception as e:
                print(f"Mouse move error: {e}")
    
    @staticmethod
    def GetButtonState(button):
        return Makcu._button_states.get(button, False)
    
    @staticmethod
    def StartButtonListener():
        pass  
    
    @staticmethod
    def Disconnect():
        if Makcu._controller:
            try:
                Makcu._controller.disconnect()
            except:
                pass
        if Makcu._original_handle_button_data:
            makcu.connection.SerialTransport._handle_button_data = Makcu._original_handle_button_data
            Makcu._original_handle_button_data = None
    
    @staticmethod
    def ease_out_quad(t):
        return t * (2 - t)
    
    @staticmethod
    def precise_sleep(seconds):
        if seconds <= 0:
            return
        
        if seconds < 0.001:
            end_time = time.perf_counter() + seconds
            while time.perf_counter() < end_time:
                pass
            return
        
        end_time = time.perf_counter() + seconds
        
        sleep_duration = seconds - 0.001
        if sleep_duration > 0:
            time.sleep(sleep_duration)
        
        while time.perf_counter() < end_time:
            pass
    
    @staticmethod
    def move_mouse_smoothly(dx, dy, steps=20):
        if dx == 0 and dy == 0:
            return

        current_x, current_y = 0.0, 0.0
        accumulated_x, accumulated_y = 0.0, 0.0

        for i in range(steps):
            t = (i + 1) / steps
            eased_t = Makcu.ease_out_quad(t)

            target_step_x = dx * eased_t
            target_step_y = dy * eased_t

            move_this_step_x = target_step_x - current_x
            move_this_step_y = target_step_y - current_y

            accumulated_x += move_this_step_x
            accumulated_y += move_this_step_y

            final_x = int(accumulated_x)
            final_y = int(accumulated_y)

            if final_x != 0 or final_y != 0:
                Makcu.MoveMouse(final_x, final_y)