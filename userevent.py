import datetime
from pynput import mouse

from utils import Settings, Logger
from global_controllers import gui_visible, is_acting, is_user_in_command, refresh_copilot_takeover_timer

class UserEvent:

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.current_settings = self.settings.get_settings()

        self.logger = Logger(self.settings)


    def is_user_idle(self, given_time:datetime.datetime):
        current_time = datetime.datetime.now()

        if((current_time-given_time).seconds >= self.current_settings['copilot_trigger_time_in_seconds']):
            return True
        return False
    
    def on_click(self, x, y, button, pressed):
        global refresh_copilot_takeover_timer
        global is_user_in_command

        print("mouse click event handler")
        print(button == mouse.Button.right, pressed, (not is_user_in_command))

        if button == mouse.Button.right and pressed and (not is_user_in_command):
            # self.logger.write(f"user took the control back.")
            is_user_in_command = True
            refresh_copilot_takeover_timer = True
        elif button == mouse.Button.left and pressed and is_user_in_command:
            refresh_copilot_takeover_timer = True

    def on_move(self, x, y):
        global refresh_copilot_takeover_timer
        global is_user_in_command

        # print("mouse move event handler")

        if is_user_in_command:
            refresh_copilot_takeover_timer = True
        
    def on_scroll(self, x, y, dx, dy):
        global refresh_copilot_takeover_timer
        global is_user_in_command

        # print("mouse scroll event handler")

        if is_user_in_command:
            refresh_copilot_takeover_timer = True

    # as of now the keystroke event is not getting detected
    '''
    def on_press(self, key):
        global is_user_in_command
        global refresh_copilot_takeover_timer

        print("keyboard event handler")
        if is_user_in_command:
            refresh_copilot_takeover_timer = True
    '''

