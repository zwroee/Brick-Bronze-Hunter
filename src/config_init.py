import sys

from config_handler import get_info_from_config, get_file_name_w_directory, change_resolution

class ConfigManager:
    def __init__(self):
        try:
            self.img_scale_percent = 400
            tmp = change_resolution()
            # default based on resolution
            self.target_coordinates = tmp[0]
            self.text_coords = tmp[1]
            self.hold_time = int(get_info_from_config('config.txt', "hold_time"))
            self.key_1 = get_info_from_config('config.txt', "key_1")
            self.key_2 = get_info_from_config('config.txt', "key_2")
            self.countdown_time = int(get_info_from_config('config.txt', "countdown_time"))
            self.debug = bool(get_info_from_config('config.txt', "debug"))
            self.threshold = float(get_info_from_config('config.txt', "threshold"))
            self.img_dir = get_file_name_w_directory(get_info_from_config('config.txt', "folder_path"))
            self.precheck_threshold = float(get_info_from_config('config.txt', "precheck_threshold"))
            self.discord_webhook_url = get_info_from_config('config.txt', "discord_webhook_url")
            try:
                self.discord_avatar_url = get_info_from_config('config.txt', "discord_avatar_url")
            except Exception:
                self.discord_avatar_url = ""
            # override target coordinates if explicit values exist
            try:
                tx = int(get_info_from_config('config.txt', 'target_coordinates_x'))
                ty = int(get_info_from_config('config.txt', 'target_coordinates_y'))
                if tx and ty:
                    self.target_coordinates = [tx, ty]
            except Exception:
                pass
        except Exception as e:
            print("Error: ", e)
            print("Please check your spelling dude, you probably typed something wrong in on the config file.")
            input()
            sys.exit()
def init_config():
    print("Creating configManager...")
    return ConfigManager()