import os
import math
import time
import json
import tkinter
import customtkinter
from PIL import Image

from functools import partial

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class App2(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("Developer Decoy - Configuration panel")

        # self.button = customtkinter.CTkButton(master=self, command=self.button_callback)
        # self.button.pack(padx=20, pady=20)

        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # adding scroll
        # self.scroll_bar =  customtkinter.CTkScrollbar(self)
        # self.scroll_bar.grid(row=0, column=2, rowspan=3, columnspan=1)

        ####################
        # tkinter variable #
        ####################

        ##-----
        # mouse move bias indicator variable
        self.mouse_move_bias_indicator_variable = tkinter.DoubleVar()

        # mouse move lower limit indicator variable
        self.mouse_move_speed_lower_indicator_variable = tkinter.DoubleVar()

        # mouse move upper limit indicator variable
        self.mouse_move_speed_upper_indicator_variable = tkinter.DoubleVar()

        ##-----
        # mouse click bias indicator variable
        self.mouse_click_bias_indicator_variable = tkinter.DoubleVar()

        ##----
        # mouse scroll bias indicator variable
        self.mouse_scroll_bias_indicator_variable = tkinter.DoubleVar()

        ##----
        # key stroke bias indicator variable
        self.key_stroke_bias_indicator_variable = tkinter.DoubleVar()

        # key stroke delay indicator variable
        self.key_stroke_delay_indicator_variable = tkinter.DoubleVar()

        ##-----
        # application change bias indicator variable
        self.application_change_bias_indicator_variable = tkinter.DoubleVar()
        ####################


        #####################
        # system_info_frame #
        #####################

        ## frame
        self.system_info_frame = customtkinter.CTkFrame(
                                    master=self,
                                    corner_radius=10
                                )
        self.system_info_frame.grid(row=0, column=0, columnspan=1, rowspan=1, padx=10, pady=10,sticky="ewns")
        self.system_info_frame.grid_rowconfigure(0, weight=1)
        self.system_info_frame.grid_rowconfigure(1, weight=1)
        self.system_info_frame.grid_rowconfigure(2, weight=1)
        ## frame end

        ## components
        self.screen_size_info_lable = customtkinter.CTkLabel(
                                    master=self.system_info_frame, 
                                    text="You Screen dimentions"
                                )
        self.screen_size_info_lable.grid(row=0, sticky="w", padx=10, pady=(10,5))

        self.screen_size_info_height_lable = customtkinter.CTkLabel(
                                    master=self.system_info_frame, 
                                    text=f"Height: {960} px"
                                )
        self.screen_size_info_height_lable.grid(row=1, sticky="w", padx=10, pady=(5,5))

        self.screen_size_info_widthlable = customtkinter.CTkLabel(
                                    master=self.system_info_frame, 
                                    text=f"Width: {1080} px"
                                )
        self.screen_size_info_widthlable.grid(row=2, sticky="w", padx=10, pady=(5,10))
        ## components end
        #####################


        ########################
        # logging_config_frame #
        ########################

        ## frame
        self.logging_config_frame = customtkinter.CTkFrame(
                                    master=self,
                                    corner_radius=10
                                )
        self.logging_config_frame.grid(row=0, column=1, rowspan=1, padx=10, pady=10, sticky="new")
        ## frame ends

        ## variables
        self.logging_switch_value = customtkinter.StringVar(value="off")
        ## variables end

        ## components
        self.logging_switch = customtkinter.CTkSwitch(
                                master=self.logging_config_frame, 
                                text="Logging", 
                                command=partial(self.button_callback, f"logging_switch {self.logging_switch_value.get()}"),
                                variable=self.logging_switch_value, 
                                onvalue="on", 
                                offvalue="off"
                            )
        self.logging_switch.grid(columnspan=1, padx=10, pady=10)
        ## components end
        ########################

        ######################
        # debug_config_frame #
        ######################

        ## frame
        self.debug_config_frame = customtkinter.CTkFrame(
                                    master=self,
                                    corner_radius=10
                                )
        self.debug_config_frame.grid(row=0, column=1, rowspan=1, padx=10, pady=10, sticky="sew")
        ## frame ends

        ## variables
        self.debug_switch_value = customtkinter.StringVar(value="off")
        ## variables end

        ## components
        self.debug_switch = customtkinter.CTkSwitch(
                                master=self.debug_config_frame, 
                                text="Debug", 
                                command=partial(self.button_callback, f"debug_switch {self.debug_switch_value.get()}"),
                                variable=self.debug_switch_value, 
                                onvalue="on", 
                                offvalue="off"
                            )
        self.debug_switch.grid(columnspan=1, padx=10, pady=10)
        ## components end
        ######################


        ########################
        # actions_config_frame #
        ########################

        ## frame
        self.actions_config_frame = customtkinter.CTkFrame(
                                    master=self,
                                    corner_radius=10
                                )
        self.actions_config_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ewn")
        self.actions_config_frame.grid_columnconfigure(0, weight=6)
        self.actions_config_frame.grid_columnconfigure(1, weight=4)
        ## frame ends

        ## variables
        self.mouse_move_enable_switch_value = customtkinter.StringVar(value="off")
        self.mouse_click_enable_switch_value = customtkinter.StringVar(value="off")
        self.mouse_scroll_enable_switch_value = customtkinter.StringVar(value="off")
        self.key_stroke_enable_switch_value = customtkinter.StringVar(value="off")
        self.change_application_enable_switch_value = customtkinter.StringVar(value="off")
        ## variables end

        ## components
        # mouse move switch
        self.mouse_move_enable_switch = customtkinter.CTkSwitch(
                                master=self.actions_config_frame, 
                                text="mouse move", 
                                command=partial(self.button_callback, f"mouse_move_switch {self.mouse_move_enable_switch_value.get()}"),
                                variable=self.mouse_move_enable_switch_value, 
                                onvalue="on", 
                                offvalue="off"
                            )
        self.mouse_move_enable_switch.grid(column=0, padx=10, pady=10, sticky="w")
        self.mouse_move_enable_settings_button = customtkinter.CTkButton(
                                                    self.actions_config_frame, 
                                                    text="",
                                                    image=customtkinter.CTkImage(light_image= Image.open(os.path.join(".","assets","images","icons","setting.png"))), 
                                                    command=self.mouse_move_setting_toplevel
                                                )
        self.mouse_move_enable_settings_button.grid(row=0, column=1,padx=10, pady=10, sticky="ns")
        # mouser move switch end
        
        # mouse click switch
        self.mouse_click_enable_switch = customtkinter.CTkSwitch(
                                master=self.actions_config_frame, 
                                text="mouse click", 
                                command=partial(self.button_callback, f"mouse_click_switch {self.mouse_click_enable_switch_value.get()}"),
                                variable=self.mouse_click_enable_switch_value, 
                                onvalue="on", 
                                offvalue="off"
                            )
        self.mouse_click_enable_switch.grid(columnspan=1, padx=10, pady=10, sticky="w")
        self.mouse_click_enable_settings_button = customtkinter.CTkButton(
                                                    self.actions_config_frame, 
                                                    text="",
                                                    image=customtkinter.CTkImage(
                                                        light_image= Image.open(os.path.join(".","assets","images","icons","setting.png"))), 
                                                    command=self.mouse_click_setting_toplevel
                                                )
        self.mouse_click_enable_settings_button.grid(row=1, column=1,padx=10, pady=10, sticky="ns")
        # mouse click switch end
        
        # mouse scroll switch
        self.mouse_scroll_enable_switch = customtkinter.CTkSwitch(
                                master=self.actions_config_frame, 
                                text="mouse scroll", 
                                command=partial(self.button_callback, f"mouse_scroll_switch {self.mouse_scroll_enable_switch_value.get()}"),
                                variable=self.mouse_scroll_enable_switch_value, 
                                onvalue="on", 
                                offvalue="off"
                            )
        self.mouse_scroll_enable_switch.grid(columnspan=1, padx=10, pady=10, sticky="w")
        self.mouse_scroll_enable_settings_button = customtkinter.CTkButton(
                                                    self.actions_config_frame, 
                                                    text="",
                                                    image=customtkinter.CTkImage(light_image= Image.open(os.path.join(".","assets","images","icons","setting.png"))), 
                                                    command=self.mouse_scroll_setting_toplevel
                                                )
        self.mouse_scroll_enable_settings_button.grid(row=2, column=1,padx=10, pady=10, sticky="ns")
        # mouse scroll switch end
        
        # key stroke switch
        self.key_stroke_enable_switch = customtkinter.CTkSwitch(
                                master=self.actions_config_frame, 
                                text="key stroke", 
                                command=partial(self.button_callback, f"key_stroke_enable_switch {self.key_stroke_enable_switch_value.get()}"),
                                variable=self.key_stroke_enable_switch_value, 
                                onvalue="on", 
                                offvalue="off"
                            )
        self.key_stroke_enable_switch.grid(columnspan=1, padx=10, pady=10, sticky="w")
        self.key_stroke_enable_settings_button = customtkinter.CTkButton(
                                                    self.actions_config_frame, 
                                                    text="",
                                                    image=customtkinter.CTkImage(light_image= Image.open(os.path.join(".","assets","images","icons","setting.png"))), 
                                                    command=self.key_stroke_setting_toplevel
                                                )
        self.key_stroke_enable_settings_button.grid(row=3, column=1,padx=10, pady=10, sticky="ns")
        # key stroke switch end
        
        # change application switch
        self.change_application_enable_switch = customtkinter.CTkSwitch(
                                master=self.actions_config_frame, 
                                text="change application", 
                                command=partial(self.button_callback, f"change_application_enable_switch {self.change_application_enable_switch_value.get()}"),
                                variable=self.change_application_enable_switch_value, 
                                onvalue="on", 
                                offvalue="off"
                            )
        self.change_application_enable_switch.grid(columnspan=1, padx=10, pady=10, sticky="w")
        self.change_application_settings_button = customtkinter.CTkButton(
                                                    self.actions_config_frame, 
                                                    text="",
                                                    image=customtkinter.CTkImage(light_image= Image.open(os.path.join(".","assets","images","icons","setting.png"))), 
                                                    command=self.application_change_setting_toplevel
                                                )
        self.change_application_settings_button.grid(row=4, column=1,padx=10, pady=10, sticky="ns")
        # change application switch end
        ## components end
        ########################


    ## methods
    def update_settings( self, updated_setting_dict) -> None:
        setting_file = open("settings_test.json", "r")
        all_settings = json.loads(setting_file.read())
        for setting in updated_setting_dict:
            all_settings[setting] = updated_setting_dict[setting]
        setting_file.close()

        setting_file = open("settings_test.json", "w")
        updated_setting = json.dumps(all_settings)
        for character in updated_setting:
            setting_file.write(character)

            if character == ",":
                setting_file.write("\n")

        setting_file.close()

    def button_callback(self, message):
        print(f"{message} used")

    def slider_event(self, value):
        value = math.floor(value)
        print(value)
    
        


    ## additional windows
    def mouse_move_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("action: mouse move configuration")
        # window.geometry("400x200")

        ## mouse move bias configuration
        mouse_move_bias_label = customtkinter.CTkLabel(window, text="mouse move action bias")
        mouse_move_bias_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # mouse move bias indicator
        mouse_move_bias_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.mouse_move_bias_indicator_variable)
        mouse_move_bias_indicator_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        # mouse move bias slider
        mouse_move_bias_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=1, 
                                to=10, 
                                variable=self.mouse_move_bias_indicator_variable,
                                number_of_steps=9, 
                                command=partial(self.slider_event)
                            )
        mouse_move_bias_slider.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ## mouse move lower limit configuration
        mouse_move_speed_lower_label = customtkinter.CTkLabel(window, text="mouse move speed lower limit")
        mouse_move_speed_lower_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        # mouse move lower limit indicator 
        mouse_move_speed_lower_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.mouse_move_speed_lower_indicator_variable)
        mouse_move_speed_lower_indicator_entry.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        # mouse move lower limit slider
        mouse_move_speed_lower_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=0.1, 
                                to=1, 
                                variable=self.mouse_move_speed_lower_indicator_variable,
                                number_of_steps=9, 
                                command=partial(self.slider_event)
                            )
        mouse_move_speed_lower_slider.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ## mouse move upper limit configuration
        mouse_move_speed_upper_label = customtkinter.CTkLabel(window, text="mouse move speed upper limit")
        mouse_move_speed_upper_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        # mouse move upper limit indicator 
        mouse_move_speed_upper_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.mouse_move_speed_upper_indicator_variable)
        mouse_move_speed_upper_indicator_entry.grid(row=4, column=1, padx=10, pady=5, sticky="e")
        # mouse move upper limit slider
        mouse_move_speed_upper_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=0.1, 
                                to=1, 
                                variable=self.mouse_move_speed_upper_indicator_variable,
                                number_of_steps=9, 
                                command=partial(self.slider_event)
                            )
        mouse_move_speed_upper_slider.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ## instruction note label
        note_label = customtkinter.CTkLabel(
                                    master=window, 
                                    text="note: To make mouse movement look more real,there must be variation in mouse movement speed. The program will take a random speed between lower limit and upper limit.",
                                    wraplength=400,
                                    text_color="#ffff88"
                                    )
        note_label.grid(row=6, columnspan=2, padx=10, pady=20, sticky="w")

        # save button
        button = customtkinter.CTkButton(master=window,
                                 corner_radius=8,
                                 text="Save",
                                 command=self.button_callback)
        button.grid(row=7, columnspan=2, padx=10, pady=10, sticky="ewns")

    def mouse_click_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("action: mouse click configuration")

        ## mouse click bias configuration
        mouse_click_bias_label = customtkinter.CTkLabel(window, text="mouse click action bias")
        mouse_click_bias_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # mouse click bias indicator
        mouse_click_bias_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.mouse_click_bias_indicator_variable)
        mouse_click_bias_indicator_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        # mouse click bias slider
        mouse_click_bias_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=1, 
                                to=10, 
                                variable=self.mouse_click_bias_indicator_variable,
                                number_of_steps=9, 
                                command=partial(self.slider_event)
                            )
        mouse_click_bias_slider.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def mouse_scroll_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("action: mouse scroll configuration")
        
        ## mouse scroll bias configuration
        mouse_scroll_bias_label = customtkinter.CTkLabel(window, text="mouse scroll action bias")
        mouse_scroll_bias_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # mouse scroll bias indicator
        mouse_scroll_bias_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.mouse_scroll_bias_indicator_variable)
        mouse_scroll_bias_indicator_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        # mouse scroll bias slider
        mouse_scroll_bias_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=1, 
                                to=10, 
                                variable=self.mouse_scroll_bias_indicator_variable,
                                number_of_steps=9, 
                                command=partial(self.slider_event)
                            )
        mouse_scroll_bias_slider.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def key_stroke_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("action: key stroke configuration")

        ## key stroke bias configuration
        key_stroke_bias_label = customtkinter.CTkLabel(window, text="key stroke action bias")
        key_stroke_bias_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # key stroke bias indicator
        key_stroke_bias_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.key_stroke_bias_indicator_variable)
        key_stroke_bias_indicator_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        # key stroke change bias slider
        key_stroke_bias_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=1, 
                                to=10, 
                                variable=self.key_stroke_bias_indicator_variable,
                                number_of_steps=9, 
                                command=partial(self.slider_event)
                            )
        key_stroke_bias_slider.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ## key stroke delay configuration
        key_stroke_delay_label = customtkinter.CTkLabel(window, text="key stroke delay")
        key_stroke_delay_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        # key stroke delay indicator
        key_stroke_delay_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.key_stroke_delay_indicator_variable)
        key_stroke_delay_indicator_entry.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        # key stroke delay slider
        key_stroke_delay_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=1, 
                                to=5, 
                                variable=self.key_stroke_delay_indicator_variable,
                                command=partial(self.slider_event)
                            )
        key_stroke_delay_slider.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def application_change_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("action: application change configuration")

        ## application change bias configuration
        application_change_bias_label = customtkinter.CTkLabel(window, text="application change action bias")
        application_change_bias_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # application change bias indicator
        application_change_bias_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.application_change_bias_indicator_variable)
        application_change_bias_indicator_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        # application change bias slider
        application_change_bias_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=1, 
                                to=10, 
                                variable=self.application_change_bias_indicator_variable,
                                number_of_steps=9, 
                                command=partial(self.slider_event)
                            )
        application_change_bias_slider.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")


if __name__=="__main__":
    # app = App()
    # app.mainloop()
    app2 = App2()
    # app2.mainloop()

    # app2.update_settings(
    #     {
    #         "logging": "mene logging badal diya",
    #         "debug": "mene loggin bhi badal diya"
    #     }
    # )


    # while True:
    #     app2.update()