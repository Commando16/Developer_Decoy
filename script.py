import pyautogui
import json
import random
import time
import threading
from pynput import mouse
from functools import partial
import datetime

from actions import (
    randome_mouse_move,
    randome_mouse_click,
    randome_mouse_scroll,
    key_stroke,
    application_change,
)

from utils import Settings, Logger

######################
## Global variables ##
######################

refresh_copilot_takeover_timer = False
is_user_in_command = True
######################


def calculate_safe_area_bounding_box(mouse_moving_window_height:int, mouse_moving_window_width:int) -> dict:
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
    
    mouse_moving_window_bbox = {
        "x0": (screen_width - mouse_moving_window_width) // 2,
        "top": (screen_height - mouse_moving_window_height) // 2,
        "x1": ((screen_width - mouse_moving_window_width) // 2)
        + mouse_moving_window_width,
        "bottom": ((screen_height - mouse_moving_window_height) // 2)
        + mouse_moving_window_width,
        "upper_left_corner": (
            (screen_width - mouse_moving_window_width) // 2,
            (screen_height - mouse_moving_window_height) // 2,
        ),
        "upper_right_corner": (
            ((screen_width - mouse_moving_window_width) // 2)
            + mouse_moving_window_width,
            (screen_height - mouse_moving_window_height) // 2,
        ),
        "lower_left_corner": (
            (screen_width - mouse_moving_window_width) // 2,
            ((screen_height - mouse_moving_window_height) // 2)
            + mouse_moving_window_width,
        ),
        "lower_right_corner": (
            ((screen_width - mouse_moving_window_width) // 2)
            + mouse_moving_window_width,
            ((screen_height - mouse_moving_window_height) // 2)
            + mouse_moving_window_width,
        ),
    }

    return mouse_moving_window_bbox


def show_safe_box(settings_data:dict, mouse_moving_window_bbox:dict)->None:
    """
    This function will show the border of the safe area bounding box 
    """
    box_indicating_limit = settings_data["box_indicating_limit"]
    box_indicating_mouse_move_duration = settings_data["box_indicating_mouse_move_duration"]

    for itr in range(box_indicating_limit):
        pyautogui.moveTo(
            mouse_moving_window_bbox["upper_left_corner"][0],
            mouse_moving_window_bbox["upper_left_corner"][1],
            duration=box_indicating_mouse_move_duration,
        )
        pyautogui.moveTo(
            mouse_moving_window_bbox["upper_right_corner"][0],
            mouse_moving_window_bbox["upper_right_corner"][1],
            duration=box_indicating_mouse_move_duration,
        )
        pyautogui.moveTo(
            mouse_moving_window_bbox["lower_right_corner"][0],
            mouse_moving_window_bbox["lower_right_corner"][1],
            duration=box_indicating_mouse_move_duration,
        )
        pyautogui.moveTo(
            mouse_moving_window_bbox["lower_left_corner"][0],
            mouse_moving_window_bbox["lower_left_corner"][1],
            duration=box_indicating_mouse_move_duration,
        )


def is_user_idle(given_time:datetime.datetime ,idle_time_limit_in_seconds:int):
    current_time = datetime.datetime.now()

    if((current_time-given_time).seconds >= idle_time_limit_in_seconds):
        return True
    return False


def act(settings_data:dict, mouse_moving_window_bbox:dict) -> None:
    """
    This is function will act/mimic the action of developer
    """

    global refresh_copilot_takeover_timer
    global is_user_in_command

    idle_time_start = datetime.datetime.now()
    logger = Logger(settings_data)

    # actions
    enable_mouse_move = settings_data["enable_mouse_move"]
    enable_mouse_click = settings_data["enable_mouse_click"]
    enable_mouse_scroll = settings_data["enable_mouse_scroll"]
    enable_key_stroke = settings_data["enable_key_stroke"]
    enable_change_application = settings_data["enable_change_application"]

    enabled_actions_choices = []

    if enable_mouse_move:
        enabled_actions_choices = enabled_actions_choices + ["randome_mouse_move"]*settings_data["mouse_move_bias"]
    if enable_mouse_click:
        enabled_actions_choices = enabled_actions_choices + ["randome_mouse_click"]*settings_data["mouse_click_bias"]
    if enable_mouse_scroll:
        enabled_actions_choices = enabled_actions_choices + ["randome_mouse_scroll"]*settings_data["mouse_scroll_bias"]
    if enable_key_stroke:
        enabled_actions_choices = enabled_actions_choices + ["key_stroke"]*settings_data["key_stroke_bias"]
    if enable_change_application:
        enabled_actions_choices = enabled_actions_choices + ["application_change"]*settings_data["change_application_bias"]

    enabled_actions_choices_length = len(enabled_actions_choices)

    if enabled_actions_choices_length == 0:
        if settings_data["logging"]:
            logger.write("No action was enable. Script aborted")

        pyautogui.alert(
            text="No action is enabled in setting.\nEnable atleast one action.",
            title="Alert...!",
            button="OK",
        )

    else:
        print(enabled_actions_choices)
        print(enabled_actions_choices_length)

        if settings_data["enable_script_stop_timer"]:
                logger.write(f"Script stop timer is enabled. Script will be stop in {settings_data['script_stop_time_in_seconds']} seconds")

        action_start_time = datetime.datetime.now()

        while True:
            should_perform_next_move = False

            if (not settings_data["enable_copilot"]) and settings_data["enable_script_stop_timer"] and ((datetime.datetime.now()-action_start_time).total_seconds()>=settings_data["script_stop_time_in_seconds"]):
                logger.write("Scrip stopped as per timer.")
                break

            if refresh_copilot_takeover_timer:
                idle_time_start = datetime.datetime.now() #idle_time_start refreshed
                refresh_copilot_takeover_timer = False

            # deciding if the act the next move or not
            if not settings_data["enable_copilot"]:
                should_perform_next_move = True
            elif (
                settings_data["enable_copilot"] and 
                is_user_idle(given_time=idle_time_start, idle_time_limit_in_seconds=settings_data["copilot_trigger_time_in_seconds"])):
                logger.write(f"User is idle for {settings_data['copilot_trigger_time_in_seconds']}, Copilot took control.")
                is_user_in_command = False
                should_perform_next_move = True

            # print("current time idle time difference", datetime.datetime.now() - idle_time_start )
            # print("should_perform_move:", should_perform_next_move, "\n\n")

            if should_perform_next_move:
                randome_choice = random.randrange(0, enabled_actions_choices_length)
                print(randome_choice)

                if enabled_actions_choices[randome_choice] == "randome_mouse_move":
                    randome_mouse_move(
                        random.randrange(
                            mouse_moving_window_bbox["x0"], mouse_moving_window_bbox["x1"]
                        ),
                        random.randrange(
                            mouse_moving_window_bbox["top"],
                            mouse_moving_window_bbox["bottom"],
                        ),
                        random.uniform(
                            settings_data["mouse_move_duration_lower_limit"],
                            settings_data["mouse_move_duration_high_limit"]
                        ),
                        logger=logger
                    )

                elif enabled_actions_choices[randome_choice] == "randome_mouse_click":
                    randome_mouse_click(
                        random.randrange(
                            mouse_moving_window_bbox["x0"], mouse_moving_window_bbox["x1"]
                        ),
                        random.randrange(
                            mouse_moving_window_bbox["top"],
                            mouse_moving_window_bbox["bottom"],
                        ),
                        logger=logger
                    )

                elif enabled_actions_choices[randome_choice] == "randome_mouse_scroll":
                    randome_mouse_scroll(random.randrange(-15, +15), logger=logger)

                elif enabled_actions_choices[randome_choice] == "key_stroke":
                    key_stroke(settings_data["delay_between_key_stroke"], logger=logger)

                elif enabled_actions_choices[randome_choice] == "application_change":
                    application_change(logger=logger)

            time.sleep(1)

######################
## Global variables ##
######################

def on_click(x, y, button, pressed):
    global refresh_copilot_takeover_timer
    global is_user_in_command

    logger = Logger(settings_data)

    print("mouse click event handler")

    if button == mouse.Button.right and pressed and (not is_user_in_command):
        logger.write(f"user took the control back.")
        is_user_in_command = True
        refresh_copilot_takeover_timer = True
    elif button == mouse.Button.left and pressed and is_user_in_command:
        refresh_copilot_takeover_timer = True

def on_move(x, y):
    global refresh_copilot_takeover_timer
    global is_user_in_command

    print("mouse move event handler")
    if is_user_in_command:
        refresh_copilot_takeover_timer = True
    
def on_scroll(x, y, dx, dy):
    global refresh_copilot_takeover_timer

    print("mouse scroll event handler")
    if is_user_in_command:
        refresh_copilot_takeover_timer = True

def on_press(key):
    global refresh_copilot_takeover_timer

    print("keyboard event handler")
    if is_user_in_command:
        refresh_copilot_takeover_timer = True

######################

if __name__ == "__main__":

    # reading settings from settings.json
    settings = Settings()
    settings_data = settings.get_settings()

    logger = Logger(settings_data)

    print(settings_data)
    logger.write("script started")
    logger.write(f"with settings - \n{settings_data}".replace(",", "\n"))

    screen_height = pyautogui.size().height
    screen_width = pyautogui.size().width

    print(type(pyautogui.size().height))
    print(f"your screen resolution is {pyautogui.size()}")
    logger.write(f"Screen resolution is {pyautogui.size()}")

    mouse_moving_window_height = settings_data["mouse_moving_window_height"]
    mouse_moving_window_width = settings_data["mouse_moving_window_width"]

    # calculating a bounding-box in which mouse can move safely
    mouse_moving_window_bbox = calculate_safe_area_bounding_box(mouse_moving_window_height, mouse_moving_window_width)

    # showing the bounding-box borders to user
    show_safe_box(settings_data = settings_data, mouse_moving_window_bbox = mouse_moving_window_bbox)
    
    # checking with the user if the bounding-box is good for further use
    is_mouse_moving_window_bbox_correct = pyautogui.confirm(
        text="Your mouse will move in the shown area only. \nCheck if its good for your screen.",
        title="Confirm",
        buttons=["Yes", "No"],
    )

    print(is_mouse_moving_window_bbox_correct)

    if is_mouse_moving_window_bbox_correct == "Yes":
        logger.write("safe area is confirmed.")
        if settings_data["enable_copilot"]:
            logger.write("Decoy-Copilot is enabled.")
            # using pynput library mouse even detection
            try:
                mouse_event_detection_thread = mouse.Listener(
                                                    on_move=on_move,
                                                    on_click=on_click,
                                                    on_scroll=on_scroll
                                                )
                decoy_thread = threading.Thread(target=partial(act, settings_data, mouse_moving_window_bbox))

                mouse_event_detection_thread.start()
                decoy_thread.start()

                mouse_event_detection_thread.join()
                decoy_thread.join()
            except pyautogui.FailSafeException as e:
                logger.write(f"FailSafeException occurred while in Decoy-Copilot mode. MousePointer must have reached in any of four corner of your primary screen. \n {e}")
                #TODO: recalibarate mouse pointer to center
            except Exception as e:
                logger.write("exception occurred while in Decoy-Copilot mode.")
        else:
            try:
                act(
                    settings_data=settings_data, 
                    mouse_moving_window_bbox=mouse_moving_window_bbox,
                )   
            except pyautogui.FailSafeException as e:
                logger.write(f"FailSafeException occurred while in Decoy-Copilot mode. MousePointer must have reached in any of four corner of your primary screen. \n {e}")
                #TODO: recalibarate mouse pointer to center
            except Exception as e:
                print(e)
                logger.write(f"exception occurred while in Decoy-Only mode. \n {e}")
    else:
        pyautogui.alert(
            text="Change the safe box dimension in setting.\nThen run the script again.",
            title="Alert...!",
            button="OK",
        )
        logger.write("Safe area dimension were not approved. Script aborted.")
