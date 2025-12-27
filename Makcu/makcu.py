import time
import os
import sys
import io
from makcu import create_controller, MouseButton
import makcu.connection

class Makcu:
    """Wrapper class for the official makcu library to maintain API compatibility"""
    _controller = None
    _button_states = {"LMB": False, "RMB": False}
    _original_handle_button_data = None
    
    @staticmethod
    def _patched_handle_button_data(self, byte_val: int):
        """Patched version of _handle_button_data that suppresses print statements"""
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
        """Connect to the Makcu device"""
        try:
            # Patch the button handler to suppress print statements
            Makcu._original_handle_button_data = makcu.connection.SerialTransport._handle_button_data
            makcu.connection.SerialTransport._handle_button_data = Makcu._patched_handle_button_data
            
            Makcu._controller = create_controller(debug=False, auto_reconnect=True)
            
            # Set up button state monitoring
            def on_button_event(button: MouseButton, pressed: bool):
                if button == MouseButton.LEFT:
                    Makcu._button_states["LMB"] = pressed
                elif button == MouseButton.RIGHT:
                    Makcu._button_states["RMB"] = pressed
            
            Makcu._controller.set_button_callback(on_button_event)
            Makcu._controller.enable_button_monitoring(True)
            
            return True
        except Exception as e:
            # Restore original handler if connection fails
            if Makcu._original_handle_button_data:
                makcu.connection.SerialTransport._handle_button_data = Makcu._original_handle_button_data
            print(f"Makcu connection error: {str(e)}")
            return False
    
    @staticmethod
    def MoveMouse(x, y):
        """Move mouse by relative coordinates"""
        if Makcu._controller:
            try:
                Makcu._controller.move(int(x), int(y))
            except Exception as e:
                print(f"Mouse move error: {e}")
    
    @staticmethod
    def GetButtonState(button):
        """Get current button state (LMB or RMB)"""
        return Makcu._button_states.get(button, False)
    
    @staticmethod
    def StartButtonListener():
        """Button listener is automatically started on connect with the official library"""
        pass  # Already handled in Connect()
    
    @staticmethod
    def Disconnect():
        """Disconnect from the Makcu device"""
        if Makcu._controller:
            try:
                Makcu._controller.disconnect()
            except:
                pass
        # Restore original handler on disconnect
        if Makcu._original_handle_button_data:
            makcu.connection.SerialTransport._handle_button_data = Makcu._original_handle_button_data
            Makcu._original_handle_button_data = None
    
    @staticmethod
    def ease_out_quad(t):
        """Easing function for smooth movement"""
        return t * (2 - t)
    
    @staticmethod
    def move_mouse_smoothly(dx, dy, duration=0.133, steps=20):
        """Move mouse smoothly with easing - using original implementation"""
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

            # Accumulate fractional movements
            accumulated_x += move_this_step_x
            accumulated_y += move_this_step_y

            # Only move whole pixels, keep remainder for next step
            final_x = int(accumulated_x)
            final_y = int(accumulated_y)

            if final_x != 0 or final_y != 0:
                Makcu.MoveMouse(final_x, final_y)
                accumulated_x -= final_x
                accumulated_y -= final_y

            current_x = target_step_x
            current_y = target_step_y

            time.sleep(duration / steps)