import os
import time
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
        self.minsize(400, 600)

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


    ## methods

    def button_callback(self, message):
        print(f"{message} used")

    
    ## additional windows
    def mouse_move_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("400x200")

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(window, text="mouser move toplevel")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

    def mouse_click_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("400x200")

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(window, text="mouser click toplevel")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

    def mouse_scroll_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("400x200")

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(window, text="mouser scroll toplevel")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

    def key_stroke_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("400x200")

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(window, text="key stroke toplevel")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

    def application_change_setting_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("400x200")

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(window, text="application change toplevel")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)


if __name__=="__main__":
    # app = App()
    # app.mainloop()
    app2 = App2()
    app2.mainloop()

    # while True:
    #     app2.update()