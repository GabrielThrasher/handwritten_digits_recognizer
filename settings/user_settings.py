class UserSettings:
    def __init__(self):
        self.read_settings()

    def do_settings_steps(self, key_pressed):
        return key_pressed == self.settings_bind

    def do_draw_mode_steps(self, key_pressed):
        return key_pressed == self.draw_mode_bind

    def do_erase_mode_steps(self, key_pressed):
        return key_pressed == self.erase_mode_bind

    def do_reset_steps(self, key_pressed):
        return key_pressed == self.reset_bind

    def write_settings(self):
        user_settings_file = open("settings/user_settings.txt", "w")

        # Bind user settings
        user_settings_file.write(
            f"draw_mode_bind,{self.draw_mode_bind},"
            f"{self.draw_mode_exit_on_release}\n"
        )
        user_settings_file.write(
            f"erase_mode_bind,{self.erase_mode_bind},"
            f"{self.erase_mode_exit_on_release}\n"
        )
        user_settings_file.write(f"reset_bind,{self.reset_bind}\n")
        user_settings_file.write(f"settings_bind,{self.settings_bind}\n")

        # Draw style user settings
        user_settings_file.write(f"thickness,{self.thickness}\n")
        user_settings_file.write(f"num_edges,{self.num_edges}\n")
        user_settings_file.write(
            f"pressure_sensitivity,{self.pressure_sensitivity}\n"
        )

        # Theme user settings
        user_settings_file.write(f"active_bg,{self.active_background_image}\n")
        user_settings_file.write(
            f"accent_color1,{self.accent_color1[0]},{self.accent_color1[1]},"
            f"{self.accent_color1[2]}\n"
        )
        user_settings_file.write(
            f"accent_color2,{self.accent_color2[0]},{self.accent_color2[1]},"
            f"{self.accent_color2[2]}\n"
        )
        user_settings_file.write(
            f"accent_color3,{self.accent_color3[0]},{self.accent_color3[1]},"
            f"{self.accent_color3[2]}"
        )
        user_settings_file.close()

    def read_settings(self):
        user_settings_file = open("settings/user_settings.txt", "r")

        # Bind user settings
        setting = user_settings_file.readline().strip()
        setting = setting[setting.find(",") + 1:].split(",")
        self.draw_mode_bind = setting[0]
        self.draw_mode_exit_on_release = eval(setting[1])

        setting = user_settings_file.readline().strip()
        setting = setting[setting.find(",") + 1:].split(",")
        self.erase_mode_bind = setting[0]
        self.erase_mode_exit_on_release = eval(setting[1])

        setting = user_settings_file.readline().strip()
        self.reset_bind = setting[setting.find(",") + 1:]

        setting = user_settings_file.readline().strip()
        self.settings_bind = setting[setting.find(",") + 1:]

        self.bounded_keys = [self.draw_mode_bind, self.erase_mode_bind,
                             self.reset_bind, self.settings_bind]

        # Draw style user settings
        setting = user_settings_file.readline().strip()
        self.thickness = setting[setting.find(",") + 1:]

        setting = user_settings_file.readline().strip()
        self.num_edges = int(setting[setting.find(",") + 1:])

        setting = user_settings_file.readline().strip()
        self.pressure_sensitivity = eval(setting[setting.find(",") + 1:])

        # Theme user settings
        setting = user_settings_file.readline().strip()
        self.active_background_image = setting[setting.find(",") + 1:]

        setting = user_settings_file.readline().strip()
        setting = setting[setting.find(",") + 1:].split(",")
        self.accent_color1 = (int(setting[0]), int(setting[1]), int(setting[2]))

        setting = user_settings_file.readline().strip()
        setting = setting[setting.find(",") + 1:].split(",")
        self.accent_color2 = (int(setting[0]), int(setting[1]), int(setting[2]))

        setting = user_settings_file.readline().strip()
        setting = setting[setting.find(",") + 1:].split(",")
        self.accent_color3 = (int(setting[0]), int(setting[1]), int(setting[2]))

        user_settings_file.close()

    def update_settings(self):
        self.write_settings()
        self.read_settings()
