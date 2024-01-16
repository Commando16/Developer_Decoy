import pyautogui
import threading
from pynput import mouse
from functools import partial
import datetime
from tkinter import messagebox

from act import Act, UserEvent
from gui import App2, GuiHandler
from utils import Settings, Logger

from global_controllers import GlobalControllers



# Todo:
#   (Done) - Setting class
#   (Done) - Debugging and Logging (Combined)
#   (Done)[named it as Act] - Action class
#   (Done) - Make class for GUI handler
#   - make separate file for userevent (unable to achieve that as on 28-12-2023)

#   - remove debugging from the GUI (GUI is for non-technical users. So, debugging don't make sense to them and if they want they can enable it from setting file).
#   - add warnings for wrong settings.
#   - recalibrate mouse pointer to center on failsafe exception. (when corner exception occur)
#   - integrate the GUI with the main script.
#   - remove (on_move, on_scroll, on_press) event handler because they are not in use any MousePointer

# IDEAS +++++++++++++++++++++ 
#   (Done) - add a Start Decoy button/Acting GUI.
#   - add a restore default setting button GUI and argument for command line execution.
#   - remove all the unnecessary print statement.
#   - make it mac, window and linux executable.
#   - add a self destruct.
#   - add a feature where program will record the action for certain time duration and repeate the recorded action again and again.



if __name__ == "__main__":

    # initializing global controller
    global_controllers = GlobalControllers()
    
    # initializing Setting
    settings = Settings()
    current_settings = settings.get_settings()

    # initializing Logger
    logger = Logger(settings=settings)

    logger.write("script started")
    logger.write(f"with settings - \n{current_settings}".replace(",", "\n"))

    # initializing GUI handler
    gui_handler = GuiHandler(settings=settings, global_controllers=global_controllers)

    # initializing Act
    act = Act(settings=settings, global_controllers=global_controllers)

    # initalizing UserEvent
    user_event = UserEvent(settings=settings, global_controllers=global_controllers)

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
                user_mouse_event_detection_thread = mouse.Listener(
                                                    on_move=user_event.on_move,
                                                    on_click=user_event.on_click,
                                                    on_scroll=user_event.on_scroll
                                                )
                act_thread = threading.Thread(target=partial(act.act))

                gui_thread.start()
                user_mouse_event_detection_thread.start()
                act_thread.start()

                gui_thread.join()
                user_mouse_event_detection_thread.join()
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
