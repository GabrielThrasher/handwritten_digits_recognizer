from program_info.program_wide_imports import *


class Button:
    def __init__(self, game_data):
        self.game_data = game_data
        self.user_settings = self.game_data.user_settings

        self.selected_border_color = "green"
        self.hover_border_color = "blue"

        self.clicked_on_functions_map = {
            "bind": self.bind_button_clicked_on_function,
            "on_off": self.on_off_button_clicked_on_function,
            "multi_choice_type":
                self.multi_choice_type_button_clicked_on_function,
            "single_choice_type":
                self.single_choice_type_button_clicked_on_function}

        self.hover_over_functions_map = {
            "standard": self.standard_hover_button_function,
            "help": self.help_button_hover_function}

        self.normal_state_functions_map = {
            "standard": self.standard_normal_state_button_function,
            "help": self.help_button_normal_state_function}

        self.active_status_function_map = {
            "bind": self.bind_button_active_status,
            "multi_choice_type":
                self.multi_choice_type_button_active_status_function}

        self.to_return_map = {"help": False}

    def set_properties(self, name, screen, properties, text_properties,
                       description=None, alignment="top_left", radius=0,
                       hoverable=True, clickable=True):
        self.name = name
        self.screen = screen

        self.x_pos = properties[0]
        self.y_pos = properties[1]
        self.width = properties[2]
        self.height = properties[3]

        self.text = text_properties[0]
        self.font_size = text_properties[1]

        if alignment == "top_left":
            self.rect = pg.Rect(
                self.x_pos, self.y_pos, self.width,
                self.height
                )
        elif alignment == "center":
            self.rect = pg.Rect(0, 0, self.width, self.height)
            self.rect.center = (self.x_pos, self.y_pos)

        self.description = description

        self.radius = radius
        self.hoverable = hoverable
        self.clickable = clickable

        self.button_fill = "normal"
        self.text_color = "normal"

        if self.description == "theme1":
            self.normal_border_color = self.game_data.theme1_visuals[1]
        elif self.description == "theme2":
            self.normal_border_color = self.game_data.theme2_visuals[1]
        elif self.description == "theme3":
            self.normal_border_color = self.game_data.theme3_visuals[1]
        else:
            self.normal_border_color = self.user_settings.accent_color1

    def display_button(self, name, screen, mouse_pos, settings_button_clicked,
                       click_pos, properties, text_properties, description=None,
                       alignment="top_left", radius=0, hoverable=True,
                       clickable=True):
        self.set_properties(
            name, screen, properties, text_properties,
            description=description, alignment=alignment,
            radius=radius, hoverable=hoverable,
            clickable=clickable
            )

        if self.name in self.clicked_on_functions_map:
            clicked_on_function = self.clicked_on_functions_map[self.name]
        hover_over_function = self.hover_over_functions_map[
            self.name] if self.name in self.hover_over_functions_map else \
            self.hover_over_functions_map["standard"]
        normal_state_function = self.normal_state_functions_map[
            self.name] if self.name in self.normal_state_functions_map else \
            self.normal_state_functions_map["standard"]

        if (self.clickable and settings_button_clicked and
                self.rect.collidepoint(click_pos[0], click_pos[1])):
            clicked_on_function()
        elif (self.hoverable and
              self.rect.collidepoint(mouse_pos[0], mouse_pos[1])):
            hover_over_function()
        else:
            normal_state_function()

        if self.name in self.active_status_function_map:
            self.active_status_function_map[self.name]()
        self.add_button_to_screen()

        if self.name in self.to_return_map:
            return self.to_return_map[self.name]

    def standard_hover_button_function(self):
        self.border_color = self.hover_border_color

    def standard_normal_state_button_function(self):
        self.border_color = self.normal_border_color

    # Add the button the screen it's been assigned to
    def add_button_to_screen(self):
        if self.text_color == "normal":
            self.text_color = (
                self.user_settings.accent_color3)

        if self.button_fill == "normal":
            self.button_fill = self.user_settings.accent_color2
            pg.draw.rect(
                self.screen, self.button_fill, self.rect,
                border_radius=self.radius
                )
        else:
            button_surface = pg.Surface(
                (self.width, self.height),
                pg.SRCALPHA
                )
            button_surface.blit(
                self.game_data.game_images[self.button_fill + "_theme"], (0, 0)
            )
            self.screen.blit(
                button_surface, (
                    self.x_pos - self.width // 2, self.y_pos - self.height // 2)
                )

        button_rect = pg.draw.rect(
            self.screen, self.border_color, self.rect, width=2,
            border_radius=self.radius
            )
        display_text(
            screen=self.screen,
            size=self.font_size,
            message=self.text,
            RGB=self.text_color,
            position=(button_rect.centerx, button_rect.centery),
            alignment="center"
            )

    # For bind buttons
    def bind_button_clicked_on_function(self):
        self.border_color = self.selected_border_color
        if self.description == "Draw mode":
            self.game_data.update_draw_mode_key = True
            self.game_data.update_erase_mode_key = False
            self.game_data.update_reset_key = False
            self.game_data.update_settings_key = False
        elif self.description == "Erase mode":
            self.game_data.update_erase_mode_key = True
            self.game_data.update_draw_mode_key = False
            self.game_data.update_reset_key = False
            self.game_data.update_settings_key = False
        elif self.description == "Reset":
            self.game_data.update_reset_key = True
            self.game_data.update_draw_mode_key = False
            self.game_data.update_erase_mode_key = False
            self.game_data.update_settings_key = False
        elif self.description == "Settings":
            self.game_data.update_settings_key = True
            self.game_data.update_draw_mode_key = False
            self.game_data.update_erase_mode_key = False
            self.game_data.update_reset_key = False

        self.game_data.update_a_key = True

    def bind_button_active_status(self):
        if (self.description == "Draw mode" and
                self.game_data.update_draw_mode_key):
            self.border_color = self.selected_border_color
        elif (self.description == "Erase mode" and
              self.game_data.update_erase_mode_key):
            self.border_color = self.selected_border_color
        elif self.description == "Reset" and self.game_data.update_reset_key:
            self.border_color = self.selected_border_color
        elif (self.description == "Settings" and
              self.game_data.update_settings_key):
            self.border_color = self.selected_border_color

    def unselect_binds_buttons(self):
        self.game_data.update_draw_mode_key = False
        self.game_data.update_erase_mode_key = False
        self.game_data.update_reset_key = False
        self.game_data.update_settings_key = False

    # For on/off buttons
    def on_off_button_clicked_on_function(self):
        self.unselect_binds_buttons()

        if self.description == "draw_eor":
            self.user_settings.draw_mode_exit_on_release = \
                not self.user_settings.draw_mode_exit_on_release

        elif self.description == "erase_eor":
            self.user_settings.erase_mode_exit_on_release = \
                not self.user_settings.erase_mode_exit_on_release

        elif self.description == "pressure_sensitivity":
            self.user_settings.pressure_sensitivity = not (
                self.user_settings.pressure_sensitivity)

        self.user_settings.update_settings()

    # For help buttons
    def help_button_hover_function(self):
        self.border_color = self.hover_border_color
        self.to_return_map["help"] = True

    def help_button_normal_state_function(self):
        self.border_color = self.normal_border_color
        self.to_return_map["help"] = False

    # For multi choice type buttons
    def multi_choice_type_button_clicked_on_function(self):
        self.unselect_binds_buttons()

        # For thickness buttons
        if self.description == "thickness_small":
            self.user_settings.thickness = "small"
        elif self.description == "thickness_medium":
            self.user_settings.thickness = "medium"
        elif self.description == "thickness_large":
            self.user_settings.thickness = "large"

        # For number of edges buttons
        if self.description == "num_edges_none":
            self.user_settings.num_edges = 0
        elif self.description == "num_edges_some":
            self.user_settings.num_edges = 4
        elif self.description == "num_edges_all":
            self.user_settings.num_edges = 8

        # For theme buttons
        if self.description == "theme1":
            self.user_settings.active_background_image = \
                self.game_data.theme1_visuals[0]
            self.user_settings.accent_color1 = self.game_data.theme1_visuals[1]
            self.user_settings.accent_color2 = self.game_data.theme1_visuals[2]
            self.user_settings.accent_color3 = self.game_data.theme1_visuals[3]

        if self.description == "theme2":
            self.user_settings.active_background_image = \
                self.game_data.theme2_visuals[0]
            self.user_settings.accent_color1 = self.game_data.theme2_visuals[1]
            self.user_settings.accent_color2 = self.game_data.theme2_visuals[2]
            self.user_settings.accent_color3 = self.game_data.theme2_visuals[3]

        if self.description == "theme3":
            self.user_settings.active_background_image = \
                self.game_data.theme3_visuals[0]
            self.user_settings.accent_color1 = self.game_data.theme3_visuals[1]
            self.user_settings.accent_color2 = self.game_data.theme3_visuals[2]
            self.user_settings.accent_color3 = self.game_data.theme3_visuals[3]

        if self.description == "theme4":
            self.user_settings.active_background_image = \
                self.game_data.theme4_visuals[0]
            self.user_settings.accent_color1 = self.game_data.theme4_visuals[1]
            self.user_settings.accent_color2 = self.game_data.theme4_visuals[2]
            self.user_settings.accent_color3 = self.game_data.theme4_visuals[3]

        self.user_settings.update_settings()

    def multi_choice_type_button_active_status_function(self):
        # For thickness buttons
        if self.description == "thickness_small":
            if self.user_settings.thickness == "small":
                self.border_color = self.selected_border_color
        elif self.description == "thickness_medium":
            if self.user_settings.thickness == "medium":
                self.border_color = self.selected_border_color
        elif self.description == "thickness_large":
            if self.user_settings.thickness == "large":
                self.border_color = self.selected_border_color

        # For number of edges buttons
        if self.description == "num_edges_none":
            if self.user_settings.num_edges == 0:
                self.border_color = self.selected_border_color
        elif self.description == "num_edges_some":
            if self.user_settings.num_edges == 4:
                self.border_color = self.selected_border_color
        elif self.description == "num_edges_all":
            if self.user_settings.num_edges == 8:
                self.border_color = self.selected_border_color

                # For theme buttons
        if self.description == "theme1":
            self.button_fill = self.game_data.theme1_visuals[0]
            self.text_color = self.game_data.theme1_visuals[2]
            if self.game_data.theme_user_settings_equals_active_theme(
                    "theme1"
            ):
                self.border_color = self.selected_border_color

        elif self.description == "theme2":
            self.button_fill = self.game_data.theme2_visuals[0]
            self.text_color = self.game_data.theme2_visuals[2]
            if self.game_data.theme_user_settings_equals_active_theme(
                    "theme2"
            ):
                self.border_color = self.selected_border_color

        elif self.description == "theme3":
            self.button_fill = self.game_data.theme3_visuals[0]
            self.text_color = self.game_data.theme3_visuals[2]
            if self.game_data.theme_user_settings_equals_active_theme(
                    "theme3"
            ):
                self.border_color = self.selected_border_color

        elif self.description == "theme4":
            self.button_fill = self.game_data.theme4_visuals[0]
            self.text_color = self.game_data.theme4_visuals[2]
            if self.game_data.theme_user_settings_equals_active_theme(
                    "theme4"
            ):
                self.border_color = self.selected_border_color

    # For single choice type buttons
    def single_choice_type_button_clicked_on_function(self):
        if self.description == "load_recommended_draw_styles":
            self.user_settings.thickness = "medium"
            self.user_settings.num_edges = 8
            self.user_settings.pressure_sensitivity = True
            self.user_settings.update_settings()
