from gui.grid.grid_gui import GridGUI
from gui.non_grid.non_grid_gui import NonGridGUI
from settings.settings_window import *


class Screen:
    def __init__(self):
        self.game_data = ProgramData()
        self.game_data.load_all_images()
        self.user_settings = self.game_data.user_settings

        self.non_grid_UI = NonGridGUI(self.game_data)
        self.grid_UI = GridGUI(self.game_data)
        self.settings_window = SettingsWindow(self.game_data)

        self.grid_UI.generate_cells()
        self.running = True
        self.settings_button_clicked = False
        self.click_pos = (-1, -1)
        self.key_pressed = None

    def run(self):
        # Game loop 
        while self.running:
            # Update screen visuals
            self.game_data.get_updated_user_settings()
            self.non_grid_UI.display_background()
            self.grid_UI.display_all_cells()
            self.non_grid_UI.display_outer_border()
            self.settings_button_clicked = False

            # For loop through the event queue   
            for event in pg.event.get():
                self.mouse_pos = pg.mouse.get_pos()

                # Check for QUIT event       
                if event.type == pg.QUIT:
                    self.running = False

                # Check if keyboard or mouse was pressed
                if (event.type == pg.KEYDOWN or event.type ==
                        pg.MOUSEBUTTONDOWN):
                    # Updating a bind button
                    if self.game_data.update_a_key:
                        if event.type == pg.KEYDOWN:
                            try:
                                if event.key == pg.K_ESCAPE:
                                    self.game_data.update_a_key = False
                                    do_next_steps = False
                                else:
                                    key = chr(event.key)
                                    do_next_steps = True
                            except:
                                do_next_steps = False
                                self.game_data.update_a_key = False
                                self.key_pressed = None

                        elif event.type == pg.MOUSEBUTTONDOWN:
                            key = self.game_data.mouse_num_to_button_map[
                                event.button]
                            do_next_steps = True

                        if do_next_steps:
                            if key not in self.user_settings.bounded_keys:
                                if self.game_data.update_draw_mode_key:
                                    self.user_settings.draw_mode_bind = key
                                    self.game_data.update_draw_mode_key = False
                                elif self.game_data.update_erase_mode_key:
                                    self.user_settings.erase_mode_bind = key
                                    self.game_data.update_erase_mode_key = False
                                elif self.game_data.update_reset_key:
                                    self.user_settings.reset_bind = key
                                    self.game_data.update_reset_key = False
                                elif (self.game_data.update_settings_key and
                                      key !=
                                      self.game_data.mouse_num_to_button_map[
                                          1]):
                                    self.user_settings.settings_bind = key
                                    self.game_data.update_settings_key = False

                            self.game_data.update_a_key = False
                            self.user_settings.update_settings()

                            # Getting normal user input
                    else:
                        if event.type == pg.KEYDOWN:
                            try:
                                self.key_pressed = chr(event.key)
                            except:
                                self.key_pressed = None
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            if (self.game_data.settings_window_open and
                                    event.button == 1):
                                self.settings_button_clicked = not (
                                    self.settings_button_clicked)
                                self.click_pos = pg.mouse.get_pos()
                                self.key_pressed = None
                            else:
                                self.key_pressed = \
                                    self.game_data.mouse_num_to_button_map[
                                        event.button]

                    # Change settings mode status
                    if self.user_settings.do_settings_steps(self.key_pressed):
                        self.game_data.settings_window_open = not (
                            self.game_data.settings_window_open)
                        self.game_data.draw_mode = False
                        self.game_data.erase_mode = False

                    # If not in the settings window, change draw mode status
                    if (not self.game_data.settings_window_open) and (
                            self.user_settings.do_draw_mode_steps(
                                self.key_pressed)):
                        self.game_data.draw_mode = not self.game_data.draw_mode
                        self.game_data.erase_mode = False

                    # If not in the settings window, change erase mode status
                    if (not self.game_data.settings_window_open) and (
                            self.user_settings.do_erase_mode_steps(
                                self.key_pressed)):
                        self.game_data.erase_mode = not (
                            self.game_data.erase_mode)
                        self.game_data.draw_mode = False

                    # If not in the settings window, reset the board (change
                    # all cells to the unfilled color)
                    if (not self.game_data.settings_window_open) and (
                            self.user_settings.do_reset_steps(
                                self.key_pressed)):
                        self.grid_UI.fill_all_cells(False)
                        self.non_grid_UI.update_sidebar_stats("zeros")

                        # Used if exit on release is on for at least either
                        # draw mode or erase mode
                elif (event.type == pg.KEYUP or event.type ==
                      pg.MOUSEBUTTONUP):
                    if ((self.game_data.draw_mode and
                        self.user_settings.draw_mode_exit_on_release) or
                        (self.game_data.erase_mode and
                         self.user_settings.erase_mode_exit_on_release)):
                        if event.type == pg.KEYUP:
                            try:
                                self.key_pressed = chr(event.key)
                            except:
                                self.key_pressed = None
                        elif event.type == pg.MOUSEBUTTONUP:
                            self.key_pressed = \
                                self.game_data.mouse_num_to_button_map[
                                    event.button]
                        else:
                            self.key_pressed = None

                            # If not in the settings window, change draw mode
                            # status
                        if (not self.game_data.settings_window_open) and (
                                self.user_settings.do_draw_mode_steps(
                                    self.key_pressed)):
                            self.game_data.draw_mode = not (
                                self.game_data.draw_mode)
                            self.game_data.erase_mode = False

                        # If not in the settings window, change erase mode
                        # status
                        if (not self.game_data.settings_window_open) and (
                                self.user_settings.do_erase_mode_steps(
                                    self.key_pressed)):
                            self.game_data.erase_mode = not (
                                self.game_data.erase_mode)
                            self.game_data.draw_mode = False

                # If in draw mode, then draw
                if (self.game_data.draw_mode and event.type ==
                        pg.MOUSEMOTION):
                    self.grid_UI.fill_cell(self.mouse_pos, True)
                    if self.grid_UI.is_empty_grid():
                        self.non_grid_UI.update_sidebar_stats("zeros")
                    else:
                        self.non_grid_UI.update_sidebar_stats("ml model")

                # If in erase mode, then erase
                if (self.game_data.erase_mode and event.type ==
                        pg.MOUSEMOTION):
                    self.grid_UI.fill_cell(self.mouse_pos, False)
                    if self.grid_UI.is_empty_grid():
                        self.non_grid_UI.update_sidebar_stats("zeros")
                    else:
                        self.non_grid_UI.update_sidebar_stats("ml model")

            # Update screen visuals
            if self.game_data.settings_window_open:
                setting_window_status = "OPENED"
            else:
                setting_window_status = "CLOSED"

            self.non_grid_UI.display_title_section(
                self.mouse_pos,
                self.settings_button_clicked,
                self.click_pos
                )
            self.non_grid_UI.display_sidebar_stats()
            if self.game_data.draw_mode:
                draw_mode_status = "ON"
            else:
                draw_mode_status = "OFF"
            if self.game_data.erase_mode:
                erase_mode_status = "ON"
            else:
                erase_mode_status = "OFF"
            self.non_grid_UI.display_action_menu_section(
                draw_mode_status, erase_mode_status, setting_window_status,
                self.mouse_pos,
                self.settings_button_clicked, self.click_pos
            )

            self.non_grid_UI.display_most_likely_section()
            self.non_grid_UI.display_model_accuracy()

            # If in settings window, then display setting options      
            if self.game_data.settings_window_open:
                self.settings_window.display_settings_window(
                    self.mouse_pos, self.settings_button_clicked,
                    self.click_pos
                )

            pg.display.flip()


if __name__ == "__main__":
    Screen().run()
