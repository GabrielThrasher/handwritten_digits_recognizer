import pygame as pg

from settings.user_settings import *


class ProgramData:
    def __init__(self):
        self.user_settings = UserSettings()
        # Cell properties
        self.cell_width = 22
        self.cell_height = self.cell_width

        # Screen properties
        # number of cells - square grid of 28x28 or 784 to match NN input
        # layer size
        self.num_hor_cells = 28
        self.num_ver_cells = self.num_hor_cells
        self.cell_matrix = []

        self.left_border_width = 20
        self.right_border_width = 170
        self.top_border_width = 35
        self.bottom_border_width = 80

        self.screen_width = (self.num_hor_cells * self.cell_width +
                             self.left_border_width + self.right_border_width)
        self.screen_height = (self.num_ver_cells * self.cell_height +
                              self.top_border_width + self.bottom_border_width)

        self.screen = pg.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.category = "Digit"
        pg.display.set_caption(
            f"Handwritten {self.category.title()} Identifier"
        )
        self.screen_font = "Arial"
        self.mouse_num_to_button_map = {1: "LC", 2: "MC", 3: "RC", 4: "SU",
                                        5: "SD", 6: "BS", 7: "TS"}

        # Setting window properties
        self.settings_window_width = 267
        self.settings_window_height = 558
        self.settings_button_clicked = False
        self.click_pos = (-1, -1)

        # For updating settings
        self.update_a_key = False
        self.update_draw_mode_key = False
        self.update_erase_mode_key = False
        self.update_reset_key = False
        self.update_settings_key = False
        self.flip_draw_eor = False
        self.flip_erase_eor = False
        self.update_pressure_sensitivity = False

        # Theme properties
        self.theme_button_width = 100
        self.theme_button_height = 25
        self.theme1_visuals = ["concrete background", (75, 75, 75),
                               (180, 180, 180), (75, 75, 75)]
        self.theme2_visuals = ["wooden background", (14, 33, 22),
                               (255, 255, 255), (14, 33, 22)]
        self.theme3_visuals = ["water background", (0, 0, 21), (0, 0, 0),
                               (200, 200, 200)]
        self.theme4_visuals = ["storm background", (0, 13, 0), (255, 255, 255),
                               (0, 0, 0)]

        # Sidebar properties
        self.sidebar_image_width = 40
        self.sidebar_image_height = 43

        # Most Likely Section properties
        self.most_likely_image_width = 30
        self.most_likely_image_height = 33

        # Game images
        self.game_images = {}

        # Modes/windows
        self.settings_window_open = False
        self.draw_mode = False
        self.erase_mode = False

    def get_updated_user_settings(self):
        self.user_settings = UserSettings()

    def load_all_images(self):
        background_image_files = ["concrete background.jpg",
                                  "wooden background.jpeg",
                                  "water background.jpg",
                                  "storm background.jpg"]
        # Main screen, settings windows, and theme buttons sizes
        background_sizes = [(self.screen_width, self.screen_height), (
            self.settings_window_width, self.settings_window_height),
                            (self.theme_button_width, self.theme_button_height)]

        number_image_files = [str(x) + ".png" for x in range(10)]
        # Sidebar and most likely sizes
        number_image_sizes = [
            (self.sidebar_image_width, self.sidebar_image_height),
            (self.most_likely_image_width, self.most_likely_image_height)]

        for image_file in background_image_files:
            image = pg.image.load(
                "program_info/program_images/background_images/" +
                image_file
            ).convert_alpha()
            for i in range(len(background_sizes)):
                if i == 0:
                    background_type = "_screen"
                elif i == 1:
                    background_type = "_settings"
                elif i == 2:
                    background_type = "_theme"
                key = image_file[:image_file.rfind(".")] + background_type
                self.game_images[key] = pg.transform.scale(
                    image, (
                        background_sizes[i][0], background_sizes[i][1])
                    )

        for image_file in number_image_files:
            image = pg.image.load(
                "program_info/program_images/sidebar_images/" +
                image_file
            ).convert_alpha()
            for i in range(len(number_image_sizes)):
                if i == 0:
                    non_grid_gui_type = "_sidebar"
                elif i == 1:
                    non_grid_gui_type = "_most_likely"
                key = image_file[:image_file.rfind(".")] + non_grid_gui_type
                self.game_images[key] = pg.transform.scale(
                    image, (
                        number_image_sizes[i][0], number_image_sizes[i][1])
                    )

    def theme_user_settings_equals_active_theme(self, theme):
        if theme == "theme1":
            theme_visuals = self.theme1_visuals
        elif theme == "theme2":
            theme_visuals = self.theme2_visuals
        elif theme == "theme3":
            theme_visuals = self.theme3_visuals
        elif theme == "theme4":
            theme_visuals = self.theme4_visuals

        return ([self.user_settings.active_background_image,
                 self.user_settings.accent_color1,
                 self.user_settings.accent_color2,
                 self.user_settings.accent_color3] == theme_visuals)
