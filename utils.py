import json

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
