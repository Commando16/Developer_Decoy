import pyautogui
import time
from utils import Logger

def randome_mouse_move(x_coordinate, y_coordinate, duration, logger:Logger):
    print("randome_mouse_move", duration)
    logger.write(f"mouse moved. \nx={x_coordinate} y={y_coordinate} duration={duration}")
    pyautogui.moveTo(x_coordinate, y_coordinate, duration=duration)


def randome_mouse_click(x_coordinate, y_coordinate, logger:Logger):
    print("mouse_click")
    logger.write(f"mouse clicked. \nx={x_coordinate} y={y_coordinate}")
    pyautogui.click(x_coordinate, y_coordinate)


def randome_mouse_scroll(scroll_point, logger:Logger):
    print(f"randome_mouse_scroll {scroll_point}")
    logger.write(f"mouse scrolled. \nscroll_ticks={scroll_point}")
    pyautogui.scroll(scroll_point)


def key_stroke(delay_between_key_stroke, logger:Logger):
    print("key_stroke")
    logger.write(f"key pressed. \ndirection_key_up, direction_key_left, direction_key_right, direction_key_down")
    pyautogui.press("up")
    time.sleep(delay_between_key_stroke)
    pyautogui.press("left")
    time.sleep(delay_between_key_stroke)
    pyautogui.press("right")
    time.sleep(delay_between_key_stroke)
    pyautogui.press("down")
    time.sleep(delay_between_key_stroke)


def application_change(logger:Logger):
    print("application_change")
    logger.write(f"application changed.")
    pyautogui.keyDown("altleft")
    pyautogui.press("tab")
    pyautogui.keyUp("altleft")
