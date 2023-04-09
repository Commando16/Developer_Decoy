import json
from os import path, mkdir
from datetime import datetime

class Settings:
    def __init__(self) -> None:
        # self.setting_file_path = "settings.json"
        self.setting_file_path = "settings_test.json"
        
        f = open(self.setting_file_path)
        self.settings_data = json.load(f)
        f.close()

    def get_settings(self):
        return self.settings_data

    def update_settings(self, updated_setting_dict):
        all_settings = self.get_settings()
        for setting in updated_setting_dict:
            all_settings[setting] = updated_setting_dict[setting]

        setting_file = open(self.setting_file_path, "w")
        updated_setting = json.dumps(all_settings)
        for character in updated_setting:
            setting_file.write(character)

            if character == ",":
                setting_file.write("\n")

        setting_file.close()

class Logger:
    def __init__(self, settings_data) -> None:
        self.date_of_logging = datetime.today()
        self.settings = settings_data

        if not self.check_if_log_directory_available():
            mkdir(path.join(".", "logs"))

    def write(self, message) -> None:
        if self.settings["logging"]:
            log_file_path = path.join("logs", f"{self.date_of_logging.strftime('%b-%d-%Y')}_logs.txt")
            with open( log_file_path, "a") as log_file:
                log_file.write(f"{datetime.now()}:\n")
                log_file.write(f"{message} \n")
                log_file.write("--------------------\n\n")


    def check_if_log_directory_available(self) -> bool:
        directory_path = path.join(".", "logs")

        if path.exists(directory_path):
            return True
        return False