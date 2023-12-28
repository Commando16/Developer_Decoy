import datetime
import pyautogui
from pynput import mouse
import random
import time


from utils import Settings, Logger
from global_controllers import gui_visible, is_acting, is_user_in_command, refresh_copilot_takeover_timer

class Act:
    '''
        Act class
    '''

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.current_settings = self.settings.get_settings()

        self.logger = Logger(self.settings)

        self.screen_height = pyautogui.size().height
        self.screen_width = pyautogui.size().width

        self.enable_mouse_move = self.current_settings["enable_mouse_move"]
        self.enable_mouse_click = self.current_settings["enable_mouse_click"]
        self.enable_mouse_scroll = self.current_settings["enable_mouse_scroll"]
        self.enable_key_stroke = self.current_settings["enable_key_stroke"]
        self.enable_change_application = self.current_settings["enable_change_application"]

        self.userEvent = UserEvent(settings)

        self.mouse_moving_window_bbox = self.calculate_safe_area_bounding_box() # mouse_moving_window_bbox mean "Mouse Moving_Window Bounding Box" (the area in which the mouse will move during acting/mimicry)

    
    def calculate_safe_area_bounding_box(self) -> dict:
        """
        This method will calculate the bounding box parameter of the safe box in which the mouse moves in
        The parameter will be return in the form of a dictionary. Then result dictionary will contain the
        following parameter:

            "x0": left border location on x-axis (int)
            "top": top border location on y-axis (int)
            "x1": right border location on x-axis (int)
            "bottom": bottom border location on the y-axis (int)
            "upper_left_corner": upper left corner coordinate in (tuple)  
            "upper_right_corner": upper right corner coordinate in (tuple)
            "lower_left_corner": lower left corner coordinate in (tuple)
            "lower_right_corner": lower right corner coordinate in (tuple)
        """

        mouse_moving_window_height = self.current_settings['mouse_moving_window_height']
        mouse_moving_window_width = self.current_settings['mouse_moving_window_width']
        
        mouse_moving_window_bbox = {
            "x0": (self.screen_width - mouse_moving_window_width) // 2,
            "top": (self.screen_height - mouse_moving_window_height) // 2,
            "x1": ((self.screen_width - mouse_moving_window_width) // 2)
            + mouse_moving_window_width,
            "bottom": ((self.screen_height - mouse_moving_window_height) // 2)
            + mouse_moving_window_width,
            "upper_left_corner": (
                (self.screen_width - mouse_moving_window_width) // 2,
                (self.screen_height - mouse_moving_window_height) // 2,
            ),
            "upper_right_corner": (
                ((self.screen_width - mouse_moving_window_width) // 2)
                + mouse_moving_window_width,
                (self.screen_height - mouse_moving_window_height) // 2,
            ),
            "lower_left_corner": (
                (self.screen_width - mouse_moving_window_width) // 2,
                ((self.screen_height - mouse_moving_window_height) // 2)
                + mouse_moving_window_width,
            ),
            "lower_right_corner": (
                ((self.screen_width - mouse_moving_window_width) // 2)
                + mouse_moving_window_width,
                ((self.screen_height - mouse_moving_window_height) // 2)
                + mouse_moving_window_width,
            ),
        }

        return mouse_moving_window_bbox

    def act(self):
        """
        This is function will act/mimic the action of developer
        """

        global refresh_copilot_takeover_timer
        global is_user_in_command

        idle_time_start = datetime.datetime.now()

        # actions
        enabled_actions_choices = self.get_action_choices()
        enabled_actions_choices_length = len(enabled_actions_choices)

        if enabled_actions_choices_length == 0:
            self.logger.write("No action was enable. Script aborted")

            pyautogui.alert(
                text="No action is enabled in setting.\nEnable atleast one action.",
                title="Alert...!",
                button="OK",
            )

        else:
            print(enabled_actions_choices)
            print(enabled_actions_choices_length)

            if self.current_settings["enable_script_stop_timer"]:
                self.logger.write(f"Script stop timer is enabled. Script will be stop in {self.current_settings['script_stop_time_in_seconds']} seconds")

            action_start_time = datetime.datetime.now()

            while True:
                should_perform_next_move = False

                if (not self.current_settings["enable_copilot"]) and self.current_settings["enable_script_stop_timer"] and ((datetime.datetime.now()-action_start_time).total_seconds()>=self.current_settings["script_stop_time_in_seconds"]):
                    self.logger.write("Scrip stopped as per timer.")
                    break

                if refresh_copilot_takeover_timer:
                    idle_time_start = datetime.datetime.now() #idle_time_start refreshed
                    refresh_copilot_takeover_timer = False

                # deciding if the act the next move or not
                if not self.current_settings["enable_copilot"]:
                    should_perform_next_move = True
                elif (
                    self.current_settings["enable_copilot"] and 
                    self.userEvent.is_user_idle(given_time=idle_time_start)):
                    self.logger.write(f"User is idle for {self.current_settings['copilot_trigger_time_in_seconds']}, Copilot took control.")
                    is_user_in_command = False
                    should_perform_next_move = True

                print("current time idle time difference", datetime.datetime.now() - idle_time_start )
                print("should_perform_move:", should_perform_next_move, "\n\n")

                if should_perform_next_move:
                    random_choice = random.randrange(0, enabled_actions_choices_length)
                    print(random_choice)

                    if enabled_actions_choices[random_choice] == "random_mouse_move":
                        self.random_mouse_move(
                            random.randrange(
                                self.mouse_moving_window_bbox["x0"], self.mouse_moving_window_bbox["x1"]
                            ),
                            random.randrange(
                                self.mouse_moving_window_bbox["top"],
                                self.mouse_moving_window_bbox["bottom"],
                            ),
                            random.uniform(
                                self.current_settings["mouse_move_duration_lower_limit"],
                                self.current_settings["mouse_move_duration_high_limit"]
                            )
                        )

                    elif enabled_actions_choices[random_choice] == "random_mouse_click":
                        self.random_mouse_click(
                            random.randrange(
                               self.mouse_moving_window_bbox["x0"], self.mouse_moving_window_bbox["x1"]
                            ),
                            random.randrange(
                                self.mouse_moving_window_bbox["top"],
                                self.mouse_moving_window_bbox["bottom"],
                            )
                        )

                    elif enabled_actions_choices[random_choice] == "random_mouse_scroll":
                        self.random_mouse_scroll(random.randrange(-15, +15))

                    elif enabled_actions_choices[random_choice] == "key_stroke":
                        self.key_stroke()

                    elif enabled_actions_choices[random_choice] == "application_change":
                        self.application_change()

                time.sleep(1)

    def random_mouse_move(self, x_coordinate, y_coordinate, duration):
        """
            This function will move the mouse randomly with in safe-area
        """
        self.logger.write(f"mouse moved. \nx={x_coordinate} y={y_coordinate} duration={duration}")
        pyautogui.moveTo(x_coordinate, y_coordinate, duration=duration)


    def random_mouse_click(self, x_coordinate, y_coordinate):
        """
            This function will randomly with the click somewhere with in safe-area
        """
        self.logger.write(f"mouse clicked. \nx={x_coordinate} y={y_coordinate}")
        pyautogui.click(x_coordinate, y_coordinate)


    def random_mouse_scroll(self, scroll_point):
        """
            This function will scroll random amount of scroll ticks in either up or down direction
        """
        self.logger.write(f"mouse scrolled. \nscroll_ticks={scroll_point}")
        pyautogui.scroll(scroll_point)


    def key_stroke(self):
        """
            This function will make the key strokes.
        """

        self.logger.write(f"key pressed. \ndirection_key_up, direction_key_left, direction_key_right, direction_key_down")
        pyautogui.press("up")
        time.sleep(self.current_settings['delay_between_key_stroke'])
        pyautogui.press("left")
        time.sleep(self.current_settings['delay_between_key_stroke'])
        pyautogui.press("right")
        time.sleep(self.current_settings['delay_between_key_stroke'])
        pyautogui.press("down")
        time.sleep(self.current_settings['delay_between_key_stroke'])


    def application_change(self):
        """
            This function will change the currently opened application.
        """

        self.logger.write(f"application changed.")
        pyautogui.keyDown("altleft")
        pyautogui.press("tab")
        pyautogui.keyUp("altleft")

    
    def get_action_choices(self) -> list:
        """
            This function will get the enabled action and return an array of enabled actions.
        """

        actions_choices = []
        
        if self.enable_mouse_move:
            actions_choices = actions_choices + ["random_mouse_move"]*self.current_settings["mouse_move_bias"]
        if self.enable_mouse_click:
            actions_choices = actions_choices + ["random_mouse_click"]*self.current_settings["mouse_click_bias"]
        if self.enable_mouse_scroll:
            actions_choices = actions_choices + ["random_mouse_scroll"]*self.current_settings["mouse_scroll_bias"]
        if self.enable_key_stroke:
            actions_choices = actions_choices + ["key_stroke"]*self.current_settings["key_stroke_bias"]
        if self.enable_change_application:
            actions_choices = actions_choices + ["application_change"]*self.current_settings["change_application_bias"]

        return actions_choices
    
    def show_safe_box(self)->None:
        """
        This function will show the border of the safe area bounding box 
        """
        box_indicating_limit = self.current_settings["box_indicating_limit"]
        box_indicating_mouse_move_duration = self.current_settings["box_indicating_mouse_move_duration"]

        for itr in range(box_indicating_limit):
            pyautogui.moveTo(
                self.mouse_moving_window_bbox["upper_left_corner"][0],
                self.mouse_moving_window_bbox["upper_left_corner"][1],
                duration=box_indicating_mouse_move_duration,
            )
            pyautogui.moveTo(
                self.mouse_moving_window_bbox["upper_right_corner"][0],
                self.mouse_moving_window_bbox["upper_right_corner"][1],
                duration=box_indicating_mouse_move_duration,
            )
            pyautogui.moveTo(
                self.mouse_moving_window_bbox["lower_right_corner"][0],
                self.mouse_moving_window_bbox["lower_right_corner"][1],
                duration=box_indicating_mouse_move_duration,
            )
            pyautogui.moveTo(
                self.mouse_moving_window_bbox["lower_left_corner"][0],
                self.mouse_moving_window_bbox["lower_left_corner"][1],
                duration=box_indicating_mouse_move_duration,
            )


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

        if button == mouse.Button.right and pressed and (not is_user_in_command):
            self.logger.write(f"user took the control back.")
            is_user_in_command = True
            refresh_copilot_takeover_timer = True
        elif button == mouse.Button.left and pressed and is_user_in_command:
            refresh_copilot_takeover_timer = True

    def on_move(self, x, y):
        global refresh_copilot_takeover_timer
        global is_user_in_command

        if is_user_in_command:
            refresh_copilot_takeover_timer = True
        
    def on_scroll(self, x, y, dx, dy):
        global refresh_copilot_takeover_timer

        if is_user_in_command:
            refresh_copilot_takeover_timer = True

    # as of now the keystroke event is not getting detected
    '''
    def on_press(self, key):
        global refresh_copilot_takeover_timer

        print("keyboard event handler")
        if is_user_in_command:
            refresh_copilot_takeover_timer = True
    '''

