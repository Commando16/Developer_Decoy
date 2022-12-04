Welcome! Developer_decoy is a tool to, decoy developers persence to a system tracker.

features - 
    - mouse move
    - mouse click
    - mouse scroll
    - keystroke
    - application change

the best part is you can choose which action to keep on and which all to keep off as per the requirement of senerio.

How it works
    There is a safe window in which your mouse will move and clicks. This window will always be in the middle of the screen.You can't change the position of the window, although you can set the dimension(height and width) of it. The two following setting are for the same.

        mouse_moving_window_height
        mouse_moving_window_width

    to indicate this box to you, the mouse pointer will automatically move along side the boundries of box 2 times.
    But you can change how many time it indicate the box(revolve around the border of safe box) in the settings. And you can chenge the mouse moving speed with also. The following setting is for the same.

        box_indicating_limit
        box_indicating_mouse_move_duration

    program will then ask for if you are satisfied with the safe box dimention. If you are not click "no" and change settings again and run the script again.

    From here the script is completely automated and need no human intervention. All the action taken by script is based on what settings are there in settings.json file.
        

How to configure the setting file
    To configue this script accouding to your need, you have to add settings to your settings.json file 

    - to change height of safe window
    mouse_moving_window_height:<set some integer value here>

    - to change width of the safe window
    mouse_moving_window_width:<set some integer value here>
    


