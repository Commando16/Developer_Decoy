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

    def __init__(self, setting_file_path):
        super().__init__()
        self.setting_file_path = setting_file_path
        self.title("Developer Decoy - Configuration panel")

        self.actual_screen_height = 1080
        self.actual_screen_width = 960 

        # self.button = customtkinter.CTkButton(master=self, command=self.button_callback)
        # self.button.pack(padx=20, pady=20)

        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # adding scroll
        # self.scroll_bar =  customtkinter.CTkScrollbar(self)
        # self.scroll_bar.grid(row=0, column=2, rowspan=3, columnspan=1)

        ####################
        # tkinter variable #
        ####################

        ## debug frame tkinter variable -----------------------------------
        self.debug_switch_value = customtkinter.StringVar(value="off")

        ## logging frame tkinter variable ---------------------------------
        self.logging_switch_value = customtkinter.StringVar(value="off")

        ## action frame tkinter variable ----------------------------------
        self.mouse_move_enable_switch_value = customtkinter.StringVar(value="off")
        self.mouse_click_enable_switch_value = customtkinter.StringVar(value="off")
        self.mouse_scroll_enable_switch_value = customtkinter.StringVar(value="off")
        self.key_stroke_enable_switch_value = customtkinter.StringVar(value="off")
        self.change_application_enable_switch_value = customtkinter.StringVar(value="off")

        ## safe area tkinter variable -------------------------------------
        self.safe_area_height_value = customtkinter.IntVar()
        self.safe_area_width_value = customtkinter.IntVar()

        ## mouse move tkinter variable ------------------------------------
        # mouse move bias indicator variable
        self.mouse_move_bias_indicator_variable = tkinter.DoubleVar()

        # mouse move lower limit indicator variable
        self.mouse_move_speed_lower_indicator_variable = tkinter.DoubleVar()

        # mouse move upper limit indicator variable
        self.mouse_move_speed_upper_indicator_variable = tkinter.DoubleVar()

        ## mouse click tkinter variable -----------------------------------
        # mouse click bias indicator variable
        self.mouse_click_bias_indicator_variable = tkinter.DoubleVar()

        ## mouse scroll tkinter variable ----------------------------------
        # mouse scroll bias indicator variable
        self.mouse_scroll_bias_indicator_variable = tkinter.DoubleVar()

        ## key stroke tkinter variable ------------------------------------
        # key stroke bias indicator variable
        self.key_stroke_bias_indicator_variable = tkinter.DoubleVar()

        # key stroke delay indicator variable
        self.key_stroke_delay_indicator_variable = tkinter.DoubleVar()

        ## application change tkinter variable ----------------------------
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

        ## components
        self.logging_switch = customtkinter.CTkSwitch(
                                master=self.logging_config_frame, 
                                text="Logging", 
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

        ## components
        self.debug_switch = customtkinter.CTkSwitch(
                                master=self.debug_config_frame, 
                                text="Debug", 
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

        ## components
        # mouse move switch
        self.mouse_move_enable_switch = customtkinter.CTkSwitch(
                                master=self.actions_config_frame, 
                                text="mouse move", 
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


        ##########################
        # safe_area_config_frame #
        ##########################

        ## frame
        self.safe_area_config_frame = customtkinter.CTkFrame(
                                    master=self,
                                    corner_radius=10
                                )
        self.safe_area_config_frame.grid(columnspan=2, padx=10, pady=10, sticky="ewns")
        ## frame ends

        ## components
        self.safe_area_info_lable = customtkinter.CTkLabel(
                                    master=self.safe_area_config_frame, 
                                    text="You safe area dimentions"
                                )
        self.safe_area_info_lable.grid(column=0, row=0, sticky="w", padx=10, pady=(10,5))

        self.safe_area_height_lable = customtkinter.CTkLabel(
                                    master=self.safe_area_config_frame, 
                                    text=f"Height: {self.safe_area_height_value.get()} px"
                                )
        self.safe_area_height_lable.grid(column=0, row=1, sticky="w", padx=10, pady=(5,5))

        self.safe_area_width_lable = customtkinter.CTkLabel(
                                    master=self.safe_area_config_frame, 
                                    text=f"Width: {self.safe_area_width_value.get()} px"
                                )
        self.safe_area_width_lable.grid(column=0, row=2, sticky="w", padx=10, pady=(5,5))


        self.safe_area_settings_button = customtkinter.CTkButton(
                                                    self.safe_area_config_frame, 
                                                    text="",
                                                    image=customtkinter.CTkImage(
                                                        light_image= Image.open(os.path.join(".","assets","images","icons","setting.png"))), 
                                                    command=self.safe_area_setting_toplevel
                                        )
        self.safe_area_settings_button.grid(column=1, row=0, rowspan=3, padx=10, pady=10, sticky="ewns")
        

        ## components end
        ######################

        ###########################
        # main config save button #
        ###########################
        # save button
        self.save_button = customtkinter.CTkButton(master=self,
                                 corner_radius=8,
                                 text="Save",
                                 command=self.general_update_setting)
        self.save_button.grid(row=3, columnspan=2, padx=10, pady=10, sticky="ewns")
        # save button end

        #---------------------------#
        # initializing the settings #
        #---------------------------#
        self.initiate_setting_variable()
        #############################

    ## methods
    # initiating methods
    def initiate_setting_variable(self)-> None:
        setting_file = open(self.setting_file_path, "r")
        all_settings = json.loads(setting_file.read())

        #-----
        self.safe_area_height_value.set(all_settings["mouse_moving_window_height"])
        self.safe_area_width_value.set(all_settings["mouse_moving_window_width"])
        self.safe_area_height_lable.configure(text=f"Height: {self.safe_area_height_value.get()} px")
        self.safe_area_width_lable.configure(text=f"Width: {self.safe_area_width_value.get()} px")

        #-----
        self.debug_switch_value.set("on") if all_settings["debug"] else self.debug_switch_value.set("off")
        self.logging_switch_value.set("on") if all_settings["logging"] else self.logging_switch_value.set("off")
        #-----
        self.mouse_move_enable_switch_value.set("on") if all_settings["enable_mouse_move"] else self.mouse_move_enable_switch_value.set("off")
        self.mouse_click_enable_switch_value.set("on") if all_settings["enable_mouse_click"] else self.mouse_click_enable_switch_value.set("off")
        self.mouse_scroll_enable_switch_value.set("on") if all_settings["enable_mouse_scroll"] else self.mouse_scroll_enable_switch_value.set("off")
        self.key_stroke_enable_switch_value.set("on") if all_settings["enable_key_stroke"] else self.key_stroke_enable_switch_value.set("off")
        self.change_application_enable_switch_value.set("on") if all_settings["enable_change_application"] else self.change_application_enable_switch_value.set("off")
        #-----
        self.mouse_move_bias_indicator_variable.set(all_settings["mouse_move_bias"])
        self.mouse_move_speed_lower_indicator_variable.set(all_settings["mouse_move_duration_lower_limit"])
        self.mouse_move_speed_upper_indicator_variable.set(all_settings["mouse_move_duration_high_limit"])
        #-----
        self.mouse_click_bias_indicator_variable.set(all_settings["mouse_click_bias"])
        #-----
        self.mouse_scroll_bias_indicator_variable.set(all_settings["mouse_scroll_bias"])
        #-----
        self.key_stroke_bias_indicator_variable.set(all_settings["key_stroke_bias"])
        self.key_stroke_delay_indicator_variable.set(all_settings["delay_between_key_stroke"])
        #-----
        self.application_change_bias_indicator_variable.set(all_settings["change_application_bias"])

        setting_file.close()

    # updating method
    def update_settings( self, updated_setting_dict) -> None:
        setting_file = open(self.setting_file_path, "r")
        all_settings = json.loads(setting_file.read())
        for setting in updated_setting_dict:
            all_settings[setting] = updated_setting_dict[setting]
        setting_file.close()

        setting_file = open(self.setting_file_path, "w")
        updated_setting = json.dumps(all_settings)
        for character in updated_setting:
            setting_file.write(character)

            if character == ",":
                setting_file.write("\n")

        setting_file.close()
    
    def general_update_setting(self)-> None:
        updated_setting_dict = {
            "enable_mouse_move": True if self.mouse_move_enable_switch_value.get() == "on" else False,
            "enable_mouse_click": True if self.mouse_click_enable_switch_value.get() == "on" else False,
            "enable_mouse_scroll": True if self.mouse_scroll_enable_switch_value.get() == "on" else False,
            "enable_key_stroke": True if self.key_stroke_enable_switch_value.get() == "on" else False,
            "enable_change_application": True if self.change_application_enable_switch_value.get() == "on" else False,
            "logging": True if self.logging_switch_value.get() == "on" else False,
            "debug": True if self.debug_switch_value.get() == "on" else False
        }

        self.update_settings(updated_setting_dict)

    def mouse_move_update_setting(self)-> None:
        mouse_move_bias = int(self.mouse_move_bias_indicator_variable.get())
        mouse_move_duration_lower_limit = round(self.mouse_move_speed_lower_indicator_variable.get(), 3)
        mouse_move_duration_high_limit = round(self.mouse_move_speed_upper_indicator_variable.get(), 3)
        
        updated_setting_dict = {
            "mouse_move_bias": mouse_move_bias,
            "mouse_move_duration_lower_limit": mouse_move_duration_lower_limit,
            "mouse_move_duration_high_limit": mouse_move_duration_high_limit
        }

        self.update_settings(updated_setting_dict)
    
    def mouse_click_update_setting(self)-> None:
        mouse_click_bias = int(self.mouse_click_bias_indicator_variable.get())
        
        updated_setting_dict = {
            "mouse_click_bias": mouse_click_bias
        }
        self.update_settings(updated_setting_dict)

    def mouse_scroll_update_setting(self)-> None:
        mouse_scroll_bias = int(self.mouse_scroll_bias_indicator_variable.get())
        
        updated_setting_dict = {
            "mouse_scroll_bias": mouse_scroll_bias
        }
        self.update_settings(updated_setting_dict)

    def key_stroke_update_setting(self)-> None:
        key_stroke_bias = int(self.key_stroke_bias_indicator_variable.get())
        delay_between_key_stroke = round(self.key_stroke_delay_indicator_variable.get(), 3)
        
        updated_setting_dict = {
            "key_stroke_bias": key_stroke_bias,
            "delay_between_key_stroke": delay_between_key_stroke,
        }

        self.update_settings(updated_setting_dict)
    
    def application_change_update_setting(self)-> None:
        change_application_bias = int(self.application_change_bias_indicator_variable.get())
        
        updated_setting_dict = {
            "change_application_bias": change_application_bias
        }

        self.update_settings(updated_setting_dict)

    def safe_area_update_setting(self)-> None:
        mouse_moving_window_height = int(self.safe_area_height_value.get())
        mouse_moving_window_width = int(self.safe_area_width_value.get())
        
        updated_setting_dict = {
            "mouse_moving_window_height" : mouse_moving_window_height,
            "mouse_moving_window_width" : mouse_moving_window_width
        }

        self.update_settings(updated_setting_dict)

    # event callback
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
                                        textvariable=self.mouse_move_bias_indicator_variable,
                                        state='disabled')
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
                                        textvariable=self.mouse_move_speed_lower_indicator_variable,
                                        state='disabled')
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
                                        textvariable=self.mouse_move_speed_upper_indicator_variable,
                                        state='disabled')
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
                                 command=self.mouse_move_update_setting)
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
                                        textvariable=self.mouse_click_bias_indicator_variable,
                                        state='disabled')
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

        # save button
        button = customtkinter.CTkButton(master=window,
                                 corner_radius=8,
                                 text="Save",
                                 command=self.mouse_click_update_setting)
        button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="ewns")

    def mouse_scroll_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("action: mouse scroll configuration")
        
        ## mouse scroll bias configuration
        mouse_scroll_bias_label = customtkinter.CTkLabel(window, text="mouse scroll action bias")
        mouse_scroll_bias_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # mouse scroll bias indicator
        mouse_scroll_bias_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.mouse_scroll_bias_indicator_variable,
                                        state='disabled')
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

        # save button
        button = customtkinter.CTkButton(master=window,
                                 corner_radius=8,
                                 text="Save",
                                 command=self.mouse_scroll_update_setting)
        button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="ewns")

    def key_stroke_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("action: key stroke configuration")

        ## key stroke bias configuration
        key_stroke_bias_label = customtkinter.CTkLabel(window, text="key stroke action bias")
        key_stroke_bias_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # key stroke bias indicator
        key_stroke_bias_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.key_stroke_bias_indicator_variable,
                                        state='disabled')
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
                                        textvariable=self.key_stroke_delay_indicator_variable,
                                        state='disabled')
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

        # save button
        button = customtkinter.CTkButton(master=window,
                                 corner_radius=8,
                                 text="Save",
                                 command=self.key_stroke_update_setting)
        button.grid(row=4, columnspan=2, padx=10, pady=10, sticky="ewns")

    def application_change_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("action: application change configuration")

        ## application change bias configuration
        application_change_bias_label = customtkinter.CTkLabel(window, text="application change action bias")
        application_change_bias_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # application change bias indicator
        application_change_bias_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.application_change_bias_indicator_variable,
                                        state='disabled')
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

        # save button
        button = customtkinter.CTkButton(master=window,
                                 corner_radius=8,
                                 text="Save",
                                 command=self.application_change_update_setting)
        button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="ewns")

    def safe_area_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.title("safe area configuration")

        ## safe area height configuration
        safe_area_height_label = customtkinter.CTkLabel(window, text="safe area height")
        safe_area_height_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        # safe area height indicator
        safe_area_height_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.safe_area_height_value,
                                        state='disabled')
        safe_area_height_indicator_entry.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        # safe area height slider
        safe_area_height_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=100, # keeping it 100 px because less then that dont make sense (mouse moving area will be too less)
                                to=self.actual_screen_height, 
                                variable=self.safe_area_height_value,
                                number_of_steps=self.actual_screen_height, 
                                command=partial(self.slider_event)
                            )
        safe_area_height_slider.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ## safe area width configuration
        safe_area_width_label = customtkinter.CTkLabel(window, text="safe area width")
        safe_area_width_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        # safe area width indicator
        safe_area_width_indicator_entry = customtkinter.CTkEntry(
                                        master=window,
                                        textvariable=self.safe_area_width_value,
                                        state='disabled')
        safe_area_width_indicator_entry.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        # safe area width slider
        safe_area_width_slider = customtkinter.CTkSlider(
                                master=window, 
                                from_=100, # keeping it 100 px because less then that dont make sense (mouse moving area will be too less)
                                to=self.actual_screen_width, 
                                variable=self.safe_area_width_value,
                                number_of_steps=self.actual_screen_width, 
                                command=partial(self.slider_event)
                            )
        safe_area_width_slider.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # save button
        button = customtkinter.CTkButton(master=window,
                                 corner_radius=8,
                                 text="Save",
                                 command=self.safe_area_update_setting)
        button.grid(row=4, columnspan=2, padx=10, pady=10, sticky="ewns")


if __name__=="__main__":
    # app = App()
    # app.mainloop()
    app2 = App2(setting_file_path="settings_test.json")
    app2.mainloop()

    # while True:
    #     app2.update()