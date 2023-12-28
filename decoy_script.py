import pyautogui
import json
import random
import time
import threading
from pynput import mouse
from functools import partial
import datetime
from tkinter import messagebox

from act import Act, UserEvent
from gui import App2, GuiHandler
from utils import Settings, Logger


# Todo:
#   (Done) - Setting class
#   (Done) - Debugging and Logging (Combined)
#   (Done)[named it as Act] - Action class
#   (Done) - Make class for GUI handler

# recalibrate mouse pointer to center (when corner exception occur)


if __name__ == "__main__":
    
    # initializing Setting
    settings = Settings()
    current_settings = settings.get_settings()

    # initializing Logger
    logger = Logger(settings=settings)

    logger.write("script started")
    logger.write(f"with settings - \n{current_settings}".replace(",", "\n"))

    # initializing GUI handler
    gui_handler = GuiHandler(settings=settings)

    # initializing Act
    act = Act(settings=settings)

    # initalizing UserEvent
    user_event = UserEvent(settings=settings)

    # checking with the user if the bounding-box is good for further use
    act.show_safe_box()
    is_mouse_moving_window_bbox_correct = pyautogui.confirm(
        text="Your mouse will move in the shown area only. \nCheck if its good for your screen.",
        title="Confirm",
        buttons=["Yes", "No"],
    )

    if is_mouse_moving_window_bbox_correct == "Yes":
        logger.write("safe area is confirmed.")

        if current_settings["enable_copilot"]:
            logger.write("Decoy-Copilot is enabled.")
            try:
                gui_thread = threading.Thread(target=gui_handler.gui_initializer)
                mouse_event_detection_thread = mouse.Listener(
                                                    on_move=user_event.on_move,
                                                    on_click=user_event.on_click,
                                                    on_scroll=user_event.on_scroll
                                                )
                act_thread = threading.Thread(target=partial(act.act))

                gui_thread.start()
                mouse_event_detection_thread.start()
                act_thread.start()

                gui_thread.join()
                mouse_event_detection_thread.join()
                act_thread.join()

            except pyautogui.FailSafeException as e:
                logger.write(f"FailSafeException occurred while in Decoy-Copilot mode. MousePointer must have reached in any of four corner of your primary screen. \n {e}")
                #TODO: recalibrate mouse pointer to center
            except Exception as e:
                logger.write("exception occurred while in Decoy-Copilot mode.")
        else:
            gui_thread = threading.Thread(target=gui_handler.gui_initializer)
            gui_thread.start()

            act_thread = threading.Thread(target=partial(act.act))
            act_thread.start()

            gui_thread.join()
            act_thread.join()

    else:
        pyautogui.alert(
            text="Change the safe box dimension in setting.\nThen run the script again.",
            title="Alert...!",
            button="OK",
        )
        logger.write("Safe area dimension were not approved. Script aborted.")
