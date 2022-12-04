import pyautogui
import time

def randome_mouse_move(x_coordinate, y_coordinate, duration):
    print("randome_mouse_move", duration)
    pyautogui.moveTo(x_coordinate, y_coordinate, duration=duration)


def randome_mouse_click(x_coordinate, y_coordinate):
    print("mouse_click")
    pyautogui.click(x_coordinate, y_coordinate)


def randome_mouse_scroll(scroll_point):
    print(f"randome_mouse_scroll {scroll_point}")
    pyautogui.scroll(scroll_point)


def key_stroke(delay_between_key_stroke):
    print("key_stroke")
    pyautogui.press("up")
    time.sleep(delay_between_key_stroke)
    pyautogui.press("left")
    time.sleep(delay_between_key_stroke)
    pyautogui.press("right")
    time.sleep(delay_between_key_stroke)
    pyautogui.press("down")
    time.sleep(delay_between_key_stroke)


def application_change():
    print("application_change")
    pyautogui.keyDown("altleft")
    pyautogui.press("tab")
    pyautogui.keyUp("altleft")
