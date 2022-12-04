import pyautogui
import json
import random
import time

from actions import (
    randome_mouse_move,
    randome_mouse_click,
    randome_mouse_scroll,
    key_stroke,
    application_change,
)


def act(settings_data:dict, mouse_moving_window_bbox:dict) -> None:
    """
    This is function will act/mimic the action of developer
    """
    # actions
    enable_mouse_move = settings_data["enable_mouse_move"]
    enable_mouse_click = settings_data["enable_mouse_click"]
    enable_mouse_scroll = settings_data["enable_mouse_scroll"]
    enable_key_stroke = settings_data["enable_key_stroke"]
    enable_change_application = settings_data["enable_change_application"]

    enabled_actions_choices = []

    if enable_mouse_move:
        enabled_actions_choices.append("randome_mouse_move")
    if enable_mouse_click:
        enabled_actions_choices.append("randome_mouse_click")
    if enable_mouse_scroll:
        enabled_actions_choices.append("randome_mouse_scroll")
    if enable_key_stroke:
        enabled_actions_choices.append("key_stroke")
    if enable_change_application:
        enabled_actions_choices.append("application_change")

    enabled_actions_choices_length = len(enabled_actions_choices)

    if enabled_actions_choices_length == 0:
        pyautogui.alert(
            text="No action is enabled in setting.\nEnable atleast one action.",
            title="Alert...!",
            button="OK",
        )

    else:
        print(enabled_actions_choices)
        print(enabled_actions_choices_length)

        while True:
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
                    )
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
                )

            elif enabled_actions_choices[randome_choice] == "randome_mouse_scroll":
                randome_mouse_scroll(random.randrange(-15, +15))

            elif enabled_actions_choices[randome_choice] == "key_stroke":
                key_stroke(settings_data["delay_between_key_stroke"])

            elif enabled_actions_choices[randome_choice] == "application_change":
                application_change()

            time.sleep(1)


if __name__ == "__main__":

    # reading settings from settings.json
    f = open("settings.json")
    settings_data = json.load(f)
    f.close()
    print(settings_data)
    screen_height = pyautogui.size().height
    screen_width = pyautogui.size().width

    print(type(pyautogui.size().height))
    print(f"your screen resolution is {pyautogui.size()}")

    mouse_moving_window_height = settings_data["mouse_moving_window_height"]
    mouse_moving_window_width = settings_data["mouse_moving_window_width"]

    # calculating a bounding-box in which mouse can move safely
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

    # showing the bounding-box borders to user
    box_indicating_limit = settings_data["box_indicating_limit"]
    box_indicating_mouse_move_duration = settings_data[
        "box_indicating_mouse_move_duration"
    ]
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

    # checking with the user if the bounding-box is good for further use
    is_mouse_moving_window_bbox_correct = pyautogui.confirm(
        text="Your mouse will move in the shown area only. \nCheck if its good for your screen.",
        title="Confirm",
        buttons=["Yes", "No"],
    )

    print(is_mouse_moving_window_bbox_correct)

    if is_mouse_moving_window_bbox_correct == "Yes":
        act(
            settings_data=settings_data, 
            mouse_moving_window_bbox=mouse_moving_window_bbox
        )
    else:
        pyautogui.alert(
            text="Change the safe box dimention in setting.\nThen run the script again.",
            title="Alert...!",
            button="OK",
        )
