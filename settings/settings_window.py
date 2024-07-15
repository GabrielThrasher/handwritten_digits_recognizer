from program_info.program_wide_imports import *


class SettingsWindow:
    def __init__(self, game_data):
        self.game_data = game_data
        self.user_settings = self.game_data.user_settings
        self.settings_window_width = self.game_data.settings_window_width
        self.settings_window_height = self.game_data.settings_window_height

        self.settings_window_left = self.game_data.left_border_width + int(
            self.game_data.num_hor_cells * self.game_data.cell_width / 2
        ) - int(self.game_data.settings_window_width / 2)
        self.settings_window_top = (self.game_data.top_border_width + int(
            self.game_data.num_ver_cells * self.game_data.cell_height / 2
        ) - int(self.game_data.settings_window_height / 2))

        # Settings window buttons
        button_names = [
            "bind_help",
            "draw_mode",
            "draw_eor",
            "erase_mode",
            "erase_eor",
            "reset",
            "settings",
            "draw_style_help",
            "thickness_small",
            "thickness_medium",
            "thickness_large",
            "num_edges_0",
            "num_edges_4",
            "num_edges_8",
            "pressure_sensitivity",
            "load_recommended_draw_styles",
            "theme_help",
            "theme1",
            "theme2",
            "theme3",
            "theme4"]

        # Stores all buttons objects that are on the settings window
        self.buttons = {}
        for button_name in button_names:
            self.buttons[button_name] = Button(self.game_data)

        self.user_setting_to_button_display_map = {True: "ON", False: "OFF"}

        # Setting window properties
        self.header_font_size = 25
        self.normal_font_size = 20
        self.small_font_size = 15

        self.bind_box_width = 50
        self.bind_box_height = 30
        self.on_off_box_width = 40
        self.on_off_box_height = 25

        self.bind_options_separator = 6
        self.bind_box_name_separator = 10
        self.section_divider = """
        ----------------------------------------------------------------"""

        self.num_of_descriptions = 3
        self.hover_status = [
            "not hovering" for _ in range(self.num_of_descriptions)]
        self.increase_height_by = 0

    def display_settings_window(
        self, mouse_pos, settings_button_clicked, click_pos):
        self.descriptions_idx = -1
        self.ver_edge_shifter = 15
        self.hor_edge_shifter = 6
        self.display_frame_visuals()
        mouse_pos = self.convert_to_settings_window_coordinates(mouse_pos)
        click_pos = self.convert_to_settings_window_coordinates(click_pos)

        # Bind section
        self.display_bind_header(mouse_pos, settings_button_clicked, click_pos)
        self.display_draw_mode_bind(
            mouse_pos, settings_button_clicked, click_pos
        )
        self.display_erase_mode_bind(
            mouse_pos, settings_button_clicked, click_pos
        )
        self.display_reset_bind(mouse_pos, settings_button_clicked, click_pos)
        self.display_settings_bind(
            mouse_pos, settings_button_clicked, click_pos
        )

        self.display_section_divider(self.ver_edge_shifter)

        # Draw style section
        self.display_draw_style_header(
            mouse_pos, settings_button_clicked, click_pos
        )
        self.display_thickness_options(
            mouse_pos, settings_button_clicked, click_pos
        )
        self.display_num_edges_options(
            mouse_pos, settings_button_clicked, click_pos
        )
        self.display_pressure_sensitivity_option(
            mouse_pos, settings_button_clicked, click_pos
        )
        self.display_load_recommended_draw_styles(
            mouse_pos, settings_button_clicked, click_pos
        )

        self.display_section_divider(self.ver_edge_shifter)

        # Theme section
        self.display_theme_header(
            mouse_pos, settings_button_clicked, click_pos
        )
        self.display_theme_options(
            mouse_pos, settings_button_clicked, click_pos
        )

        # Display settings window on main screen
        self.game_data.screen.blit(
            self.settings_window,
            (self.settings_window_left,
             self.settings_window_top)
        )

    def display_frame_visuals(self):
        background_surface = pg.Surface(
            (self.settings_window_width,
             self.settings_window_height),
            pg.SRCALPHA
            )
        background_surface.blit(
            self.game_data.game_images[
                self.user_settings.active_background_image + "_settings"],
            (0, 0)
            )
        background_surface = pg.transform.scale(
            background_surface,
            (self.settings_window_width,
             self.settings_window_height + self.increase_height_by)
        )

        self.settings_window = pg.Surface(
            (self.settings_window_width,
             self.settings_window_height + self.increase_height_by),
            pg.SRCALPHA
        )
        self.settings_window.blit(background_surface, (0, 0))
        pg.draw.rect(
            self.settings_window, self.user_settings.accent_color1,
            pg.Rect(
                0, 0, self.settings_window.get_size()[0],
                self.settings_window.get_size()[1]
                ), width=1
            )

    def convert_to_settings_window_coordinates(self, coordinates):
        if (
            self.settings_window_left < coordinates[0] <
            self.settings_window_left + self.settings_window_width) and (
            self.settings_window_top < coordinates[1] <
            self.settings_window_top + self.settings_window_height
        ):
            return (
                coordinates[0] - self.settings_window_left,
                coordinates[1] - self.settings_window_top)
        else:
            return (-1, -1)

    def display_section_divider(self, y_pos):
        # Divider for different sections of the settings menu
        divider_rect = display_text(
            screen=self.settings_window,
            size=11,
            message=self.section_divider,
            RGB=self.user_settings.accent_color2,
            position=(self.settings_window_width // 2, y_pos),
            alignment="center"
        )
        self.ver_edge_shifter += divider_rect.height + 5

    def get_description_lines(self, text, font_size, max_width):
        font = pg.font.SysFont(self.game_data.screen_font, font_size)
        words = text.split()

        lines = []
        while len(words) > 0:
            line_words = []

            while len(words) > 0:
                line_words.append(words.pop(0))
                text = font.render(
                    ' '.join(line_words + words[:1]),
                    True,
                    "white"
                )
                if text.get_rect().width > max_width:
                    break

            line = ' '.join(line_words)
            lines.append(line)

        return lines

    def display_description(self, status, on_message, off_message):
        self.descriptions_idx += 1

        if status:
            self.hover_status[self.descriptions_idx] = "hovering"
            message = self.get_description_lines(
                text=on_message, font_size=11,
                max_width=self.settings_window_width - 4
            )
        else:
            self.hover_status[self.descriptions_idx] = "not hovering"
            message = self.get_description_lines(
                text=off_message, font_size=11,
                max_width=self.settings_window_width - 4
            )

        for i in range(len(message)):
            desc_rect = display_text(
                screen=self.settings_window,
                size=11,
                message=message[i],
                RGB=self.user_settings.accent_color2,
                position=(self.settings_window_width // 2,
                          self.ver_edge_shifter - 9 + 13 * i),
                alignment="center"
            )
        self.ver_edge_shifter += len(message) * desc_rect.height - 2

        if "hovering" in self.hover_status:
            if status:
                self.increase_height_by = (len(message) - 1) * desc_rect.height
        else:
            self.increase_height_by = 0

    def display_bind_header(self, mouse_pos, settings_button_clicked,
                            click_pos):
        # Bind header and help button
        bind_rect = display_text(
            screen=self.settings_window,
            size=self.header_font_size,
            message="Binds",
            RGB=self.user_settings.accent_color2,
            position=(self.settings_window_width // 2, self.ver_edge_shifter),
            alignment="center"
        )
        self.ver_edge_shifter += bind_rect.height

        is_hovering = self.buttons["bind_help"].display_button(
            name="help",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width - 20, 4, 15, 15),
            text_properties=("?", 11),
            radius=25,
            clickable=False
        )

        self.display_description(
            status=is_hovering,
            on_message=self.section_divider +
            """ To change a bind, left-click a box to select it, then click on
            a unique key bind. Note: press ESC to deselect; some special keys
            are not supported; and a two-character key bind represents a mouse
            button. Exit on release: ON - the corresponding action mode exits
            upon key release; OFF - the key must be pressed again to exit.""",
            off_message=self.section_divider
        )

        display_text(
            screen=self.settings_window,
            size=11,
            message="Exit on release",
            RGB=self.user_settings.accent_color2,
            position=(self.settings_window_width - self.on_off_box_width - 10,
                      self.ver_edge_shifter - 4),
            alignment="center"
        )

    def display_draw_mode_bind(self, mouse_pos, settings_button_clicked,
                               click_pos):
        # Draw mode bind button, name, and exit on release button
        description = "Draw mode"

        self.buttons["draw_mode"].display_button(
            name="bind",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.hor_edge_shifter, self.ver_edge_shifter,
                        self.bind_box_width, self.bind_box_height),
            text_properties=(self.user_settings.draw_mode_bind,
                             self.normal_font_size),
            description=description
        )
        display_text(
            screen=self.settings_window,
            size=self.normal_font_size,
            message=description,
            RGB=self.user_settings.accent_color2,
            position=(self.hor_edge_shifter + self.bind_box_width +
                      self.bind_box_name_separator, self.ver_edge_shifter + (
                        self.bind_box_height - self.normal_font_size) // 2 - 2)
        )
        self.ver_edge_shifter += 4

        self.buttons["draw_eor"].display_button(
            name="on_off",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(
                self.settings_window_width -
                self.on_off_box_width -
                30,
                self.ver_edge_shifter,
                self.on_off_box_width,
                self.on_off_box_height),
            text_properties=(
                self.user_setting_to_button_display_map[
                    self.user_settings.draw_mode_exit_on_release],
                self.small_font_size),
            description="draw_eor"
        )
        self.ver_edge_shifter += (self.bind_box_height +
                                  self.bind_options_separator - 4)

    def display_erase_mode_bind(self, mouse_pos, settings_button_clicked,
                                click_pos):
        # Erase mode bind button, name, and exit on release button
        description = "Erase mode"

        self.buttons["erase_mode"].display_button(
            name="bind",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.hor_edge_shifter, self.ver_edge_shifter,
                        self.bind_box_width, self.bind_box_height),
            text_properties=(self.user_settings.erase_mode_bind,
                             self.normal_font_size),
            description=description
        )
        display_text(
            screen=self.settings_window,
            size=self.normal_font_size,
            message=description,
            RGB=self.user_settings.accent_color2,
            position=(self.hor_edge_shifter + self.bind_box_width +
                      self.bind_box_name_separator, self.ver_edge_shifter +
                      (self.bind_box_height - self.normal_font_size) // 2 - 2)
        )
        self.ver_edge_shifter += 4

        self.buttons["erase_eor"].display_button(
            name="on_off",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width - self.on_off_box_width -
                        30, self.ver_edge_shifter, self.on_off_box_width,
                        self.on_off_box_height),
            text_properties=(self.user_setting_to_button_display_map[
                                 self.user_settings.erase_mode_exit_on_release],
                             self.small_font_size),
            description="erase_eor"
        )
        self.ver_edge_shifter += (self.bind_box_height +
                                  self.bind_options_separator - 4)

    def display_reset_bind(self, mouse_pos, settings_button_clicked, click_pos):
        # Reset bind button and name
        description = "Reset"
        self.buttons["reset"].display_button(
            name="bind",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.hor_edge_shifter, self.ver_edge_shifter,
                        self.bind_box_width, self.bind_box_height),
            text_properties=(self.user_settings.reset_bind,
                             self.normal_font_size),
            description=description
        )
        display_text(
            screen=self.settings_window,
            size=self.normal_font_size,
            message=description,
            RGB=self.user_settings.accent_color2,
            position=(
                self.hor_edge_shifter +
                self.bind_box_width +
                self.bind_box_name_separator,
                self.ver_edge_shifter +
                (self.bind_box_height - self.normal_font_size) // 2 - 2)
        )
        self.ver_edge_shifter += (self.bind_box_height +
                                  self.bind_options_separator)

    def display_settings_bind(self, mouse_pos, settings_button_clicked,
                              click_pos):
        # Settings bind button and name
        description = "Settings"
        self.buttons["settings"].display_button(
            name="bind",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.hor_edge_shifter, self.ver_edge_shifter,
                        self.bind_box_width, self.bind_box_height),
            text_properties=(self.user_settings.settings_bind,
                             self.normal_font_size),
            description=description
        )
        display_text(
            screen=self.settings_window,
            size=self.normal_font_size,
            message=description,
            RGB=self.user_settings.accent_color2,
            position=(self.hor_edge_shifter + self.bind_box_width +
                      self.bind_box_name_separator, self.ver_edge_shifter +
                      (self.bind_box_height - self.normal_font_size) // 2 - 2)
        )
        self.ver_edge_shifter += (self.bind_box_height +
                                  self.bind_options_separator + 5)

    def display_draw_style_header(self, mouse_pos, settings_button_clicked,
                                  click_pos):
        # Draw styles header and help button
        draw_style_rect = display_text(
            screen=self.settings_window,
            size=self.header_font_size,
            message="Draw Styles",
            RGB=self.user_settings.accent_color2,
            position=(self.settings_window_width // 2, self.ver_edge_shifter),
            alignment="center"
        )
        self.ver_edge_shifter += draw_style_rect.height // 2 + 14

        is_hovering = self.buttons["draw_style_help"].display_button(
            name="help",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width - 20,
                        self.ver_edge_shifter - 40, 15, 15),
            text_properties=("?", 11),
            radius=25,
            clickable=False
        )

        self.display_description(
            status=is_hovering,
            on_message=self.section_divider +
            """ Style options for when in draw mode. Thickness: how big the
            drawing mark is. Number of edges: how many adjacent grid tiles to
            the drawing mark is filled in with an appropriate grayscale
            intensity level. Pressure sensitivity: On - repeatedly moving the
            mouse within the same grid tile increases the grayscale intensity
            level; OFF - such motion has no affect on the grayscale intensity
            level.""",
            off_message=self.section_divider
        )
        self.ver_edge_shifter -= 10

    def display_thickness_options(self, mouse_pos, settings_button_clicked,
                                  click_pos):
        thickness_rect = display_text(
            screen=self.settings_window,
            size=17,
            message="Thickness:",
            RGB=self.user_settings.accent_color2,
            position=(10, self.ver_edge_shifter)
        )
        self.ver_edge_shifter += thickness_rect.height + 15

        name = "multi_choice_type"
        # Thickness options
        self.buttons["thickness_small"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(55, self.ver_edge_shifter, 70, 25),
            text_properties=("Small", 18),
            description="thickness_small",
            alignment="center"
        )

        self.buttons["thickness_medium"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width // 2, self.ver_edge_shifter,
                        70, 25),
            text_properties=("Medium", 18),
            description="thickness_medium",
            alignment="center"
        )

        self.buttons["thickness_large"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width - 55, self.ver_edge_shifter,
                        70, 25),
            text_properties=("Large", 18),
            description="thickness_large",
            alignment="center"
        )
        self.ver_edge_shifter += 19

    def display_num_edges_options(self, mouse_pos, settings_button_clicked,
                                  click_pos):
        num_edges_rect = display_text(
            screen=self.settings_window,
            size=17,
            message="Number of edges:",
            RGB=self.user_settings.accent_color2,
            position=(10, self.ver_edge_shifter)
        )
        self.ver_edge_shifter += num_edges_rect.height + 15

        name = "multi_choice_type"
        # Number of edges options
        self.buttons["num_edges_0"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(55, self.ver_edge_shifter, 70, 25),
            text_properties=("None", 18),
            description="num_edges_none",
            alignment="center"
        )

        self.buttons["num_edges_4"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width // 2, self.ver_edge_shifter,
                        70, 25),
            text_properties=("Some", 18),
            description="num_edges_some",
            alignment="center"
        )

        self.buttons["num_edges_8"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width - 55, self.ver_edge_shifter,
                        70, 25),
            text_properties=("All", 18),
            description="num_edges_all",
            alignment="center"
        )
        self.ver_edge_shifter += 19

    def display_pressure_sensitivity_option(self, mouse_pos,
                                            settings_button_clicked, click_pos):
        button_display = self.user_setting_to_button_display_map[
            self.user_settings.pressure_sensitivity]

        self.ver_edge_shifter += 6
        pressure_sensitivity_rect = display_text(
            screen=self.settings_window,
            size=17,
            message="Pressure sensitivity:",
            RGB=self.user_settings.accent_color2,
            position=(10, self.ver_edge_shifter)
        )
        self.ver_edge_shifter -= 2

        self.buttons["pressure_sensitivity"].display_button(
            name="on_off",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(20 + pressure_sensitivity_rect.width,
                        self.ver_edge_shifter, self.on_off_box_width,
                        self.on_off_box_height),
            text_properties=(button_display, self.small_font_size),
            description="pressure_sensitivity"
        )
        self.ver_edge_shifter += pressure_sensitivity_rect.height + 26

    def display_load_recommended_draw_styles(self, mouse_pos,
                                             settings_button_clicked,
                                             click_pos):
        self.buttons["load_recommended_draw_styles"].display_button(
            name="single_choice_type",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.game_data.settings_window_width // 2,
                        self.ver_edge_shifter, 225, 25),
            text_properties=("Load recommended styles", 18),
            description="load_recommended_draw_styles",
            alignment="center"
        )
        self.ver_edge_shifter += 30

    def display_theme_header(self, mouse_pos, settings_button_clicked,
                             click_pos):
        # Theme header and help button
        theme_rect = display_text(
            screen=self.settings_window,
            size=self.header_font_size,
            message="Themes",
            RGB=self.user_settings.accent_color2,
            position=(self.settings_window_width // 2, self.ver_edge_shifter),
            alignment="center"
        )
        self.ver_edge_shifter += theme_rect.height // 2 - 26

        is_hovering = self.buttons["theme_help"].display_button(
            name="help",
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width - 20, self.ver_edge_shifter,
                        15, 15),
            text_properties=("?", 11),
            radius=25,
            clickable=False
        )
        self.ver_edge_shifter += 38

        self.display_description(
            status=is_hovering,
            on_message=self.section_divider +
                       " Left-click to select a theme design.",
            off_message=self.section_divider
        )

    def display_theme_options(self, mouse_pos, settings_button_clicked,
                              click_pos):
        name = "multi_choice_type"

        # Theme options
        self.ver_edge_shifter += 10
        self.buttons["theme1"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width // 4, self.ver_edge_shifter,
                        100, 25),
            text_properties=("Concrete", 20),
            description="theme1",
            alignment="center"
        )

        self.buttons["theme2"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(3 * self.settings_window_width // 4,
                        self.ver_edge_shifter, 100, 25),
            text_properties=("Wood", 20),
            description="theme2",
            alignment="center"
        )
        self.ver_edge_shifter += 40

        self.buttons["theme3"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(self.settings_window_width // 4, self.ver_edge_shifter,
                        100, 25),
            text_properties=("Water", 20),
            description="theme3",
            alignment="center"
        )

        self.buttons["theme4"].display_button(
            name=name,
            screen=self.settings_window,
            mouse_pos=mouse_pos,
            settings_button_clicked=settings_button_clicked,
            click_pos=click_pos,
            properties=(3 * self.settings_window_width // 4,
                        self.ver_edge_shifter, 100, 25),
            text_properties=("Storm", 20),
            description="theme4",
            alignment="center"
        )
