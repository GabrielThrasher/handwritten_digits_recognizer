from ml_model import machine_learning_model as ml
from program_info.program_wide_imports import *


class NonGridGUI:
    def __init__(self, game_data):
        self.game_data = game_data
        self.user_settings = self.game_data.user_settings

        button_names = ["title_help", "action_menu_help"]

        self.buttons = {}
        for button_name in button_names:
            self.buttons[button_name] = Button(self.game_data)

        # Help button properties
        self.help_button_text = "?"
        self.help_button_font_size = 11
        self.help_button_size = 15
        self.help_button_radius = 25

        # For ML results
        self.nums_percentages = [0.00 for _ in range(10)]

    def display_background(self):
        self.game_data.screen.blit(
            self.game_data.game_images[
                self.user_settings.active_background_image + "_screen"],
            (0, 0)
            )

    def display_title_section(self, mouse_pos, settings_button_clicked,
                              click_pos):
        ver_edge_shifter = 30
        title_desc_hor_separator = 3
        title_desc_ver_separator = 13

        title_rect = display_text(
            screen=self.game_data.screen,
            size=25,
            message=f"Handwritten {self.game_data.category.title()} Identifier",
            RGB=self.user_settings.accent_color2,
            position=(self.game_data.left_border_width,
                      self.game_data.top_border_width - ver_edge_shifter)
        )
        is_hovering = self.buttons["title_help"].display_button(
            name="help",
            screen=self.game_data.screen,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.game_data.left_border_width + title_rect.width +
                        title_desc_hor_separator,
                        self.game_data.top_border_width - ver_edge_shifter +
                        title_desc_ver_separator, self.help_button_size,
                        self.help_button_size),
            text_properties=(self.help_button_text, self.help_button_font_size),
            radius=self.help_button_radius,
            clickable=False
            )
        if is_hovering:
            message = (f"With its center of mass near the grid's center, "
                       f"draw your {self.game_data.category.lower()} and it "
                       f"will be deciphered!")
        else:
            message = ""

        display_text(
            screen=self.game_data.screen,
            size=11,
            message=message,
            RGB=self.user_settings.accent_color2,
            position=(self.game_data.left_border_width + title_rect.width +
                      title_desc_hor_separator + 20,
                      self.game_data.top_border_width - ver_edge_shifter +
                      title_desc_ver_separator + 1)
            )

    def display_outer_border(self):
        pg.draw.rect(
            self.game_data.screen,
            self.user_settings.accent_color1,
            pg.Rect(
                self.game_data.left_border_width - 1,
                self.game_data.top_border_width - 1,
                self.game_data.num_hor_cells *
                self.game_data.cell_width + 2,
                self.game_data.num_ver_cells *
                self.game_data.cell_height + 2
                ),
            width=1
            )

    def display_action_menu_section(self, draw_mode_status, erase_mode_status,
                                    setting_window_status, mouse_pos,
                                    settings_button_clicked, click_pos):
        is_hovering = self.buttons["action_menu_help"].display_button(
            name="help",
            screen=self.game_data.screen,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.game_data.left_border_width,
                        self.game_data.screen_height -
                        self.game_data.bottom_border_width + 3,
                        self.help_button_size, self.help_button_size),
            text_properties=(self.help_button_text, self.help_button_font_size),
            radius=self.help_button_radius,
            clickable=False
            )

        if is_hovering:
            message = ("Actions that can be performed; click the key bind shown"
                       " in parentheses")
        else:
            message = "Action Menu:"

        display_text(
            screen=self.game_data.screen,
            size=12,
            message=message,
            RGB=self.user_settings.accent_color2,
            position=(self.game_data.left_border_width + 17,
                      self.game_data.screen_height -
                      self.game_data.bottom_border_width + 4)
            )

        display_text(
            screen=self.game_data.screen,
            size=18,
            message=f"{draw_mode_status}: Draw mode ("
            f"{self.user_settings.draw_mode_bind})",
            RGB=self.user_settings.accent_color2,
            position=(self.game_data.left_border_width,
                      self.game_data.screen_height -
                      self.game_data.bottom_border_width + 23)
            )

        display_text(
            screen=self.game_data.screen,
            size=18,
            message=f"{erase_mode_status}: Erase mode ("
            f"{self.user_settings.erase_mode_bind})",
            RGB=self.user_settings.accent_color2,
            position=(self.game_data.left_border_width + 200,
                      self.game_data.screen_height -
                      self.game_data.bottom_border_width + 23)
            )

        display_text(
            screen=self.game_data.screen,
            size=18,
            message=f"Reset ({self.user_settings.reset_bind})",
            RGB=self.user_settings.accent_color2,
            position=(self.game_data.left_border_width,
                      self.game_data.screen_height -
                      self.game_data.bottom_border_width + 50)
            )

        display_text(
            screen=self.game_data.screen,
            size=18,
            message=f"{setting_window_status}: Settings ("
            f"{self.user_settings.settings_bind})",
            RGB=self.user_settings.accent_color2,
            position=(self.game_data.left_border_width + 200,
                      self.game_data.screen_height -
                      self.game_data.bottom_border_width + 50)
            )

    def display_sidebar_image(self, screen, game_data, user_settings, name,
                              x_pos, y_pos, width, height):
        pg.draw.rect(
            screen, user_settings.accent_color1,
            pg.Rect(x_pos, y_pos, width, height),
            border_radius=10
            )
        pg.draw.rect(
            screen, user_settings.accent_color2,
            pg.Rect(x_pos, y_pos, width, height), width=1,
            border_radius=10
            )
        screen.blit(game_data.game_images[name], (x_pos, y_pos))

    def display_sidebar_stats(self):
        nums = [str(x) + "_sidebar" for x in range(10)]
        spacing = self.game_data.sidebar_image_height + 20
        x_pos = (self.game_data.screen_width -
                 self.game_data.right_border_width + 5)

        for i in range(len(nums)):
            self.display_sidebar_image(
                screen=self.game_data.screen,
                game_data=self.game_data,
                user_settings=self.user_settings,
                name=nums[i],
                x_pos=x_pos,
                y_pos=self.game_data.top_border_width + spacing * i + 2,
                width=self.game_data.sidebar_image_width,
                height=self.game_data.sidebar_image_height
                )
            display_text(
                screen=self.game_data.screen,
                size=27,
                message=f"{self.nums_percentages[i]:.2f}%",
                RGB=self.game_data.user_settings.accent_color2,
                position=(x_pos + 50, self.game_data.top_border_width +
                          spacing * i + 5)
                )

    def update_sidebar_stats(self, update):
        if update == "ml model":
            ml_input = np.array([])
            for col_num in range(self.game_data.num_hor_cells):
                for row_num in range(self.game_data.num_ver_cells):
                    ml_input = np.append(ml_input,
                                         self.game_data.cell_matrix[row_num][
                                             col_num].cell_value
                                         )

            ml_results = ml.predict_number(
                ml_input.reshape(len(ml_input), 1)).tolist()
            self.nums_percentages = [round(100 * (x / sum(ml_results)), 2) for x
                                     in ml_results]

        elif update == "zeros":
            self.nums_percentages = [0.00 for _ in range(10)]

    def display_most_likely_section(self):
        display_text(
            screen=self.game_data.screen,
            size=20,
            message=f"Most-Likely {self.game_data.category.title()}:",
            RGB=self.user_settings.accent_color2,
            position=(self.game_data.left_border_width + 422,
                      self.game_data.screen_height -
                      self.game_data.bottom_border_width + 10)
            )
        # If the max value occurs more than once
        if self.nums_percentages.count(max(self.nums_percentages)) != 1:
            display_text(
                screen=self.game_data.screen,
                size=30,
                message="There's a tie",
                RGB=self.user_settings.accent_color2,
                position=(self.game_data.left_border_width + 422,
                          self.game_data.screen_height -
                          self.game_data.bottom_border_width + 36)
                )
        else:
            highest_percent_num = self.nums_percentages.index(
                max(self.nums_percentages)
            )
            self.display_sidebar_image(
                screen=self.game_data.screen,
                game_data=self.game_data,
                user_settings=self.user_settings,
                name=f"{highest_percent_num}_most_likely",
                x_pos=self.game_data.left_border_width + 422,
                y_pos=self.game_data.screen_height -
                      self.game_data.bottom_border_width + 36,
                width=self.game_data.most_likely_image_width,
                height=self.game_data.most_likely_image_height
                )
            display_text(
                screen=self.game_data.screen,
                size=30,
                message=f"at {self.nums_percentages[highest_percent_num]}%",
                RGB=self.user_settings.accent_color2,
                position=(self.game_data.left_border_width +
                          self.game_data.most_likely_image_width + 432,
                          self.game_data.screen_height -
                          self.game_data.bottom_border_width + 36)
                )

    def display_model_accuracy(self):
        display_text(
            screen=self.game_data.screen,
            size=12,
            message=f"Model accuracy: ~{ml.get_NN_model_accuracy()}%",
            RGB=self.game_data.user_settings.accent_color2,
            position=(self.game_data.screen_width - 150,
                      self.game_data.screen_height - 20)
            )
