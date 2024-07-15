from gui.grid.cell import *


class GridGUI:
    def __init__(self, game_data):
        self.game_data = game_data
        self.user_settings = self.game_data.user_settings

        if self.user_settings.num_edges == 0:
            # Num of adjacent "active" (value of 1) cells: corresponding value
            self.value_map = {0: 0, 1: 1}
            # Num of adjacent "active" (grayscale of (255, 255, 255)) cells:
            # corresponding grayscale value
            self.grayscale_map = {0: (0, 0, 0), 8: (255, 255, 255)}
        else:
            value_fraction = 1 / self.user_settings.num_edges
            grayscale_fraction = 255 / self.user_settings.num_edges

            # Num of adjacent "active" (value of 1) cells: corresponding value
            self.value_map = {i: i * value_fraction for i in
                              range(self.user_settings.num_edges + 1)}
            # Num of adjacent "active" (grayscale of (255, 255, 255)) cells:
            # corresponding grayscale value
            self.grayscale_map = {i: (i * grayscale_fraction,
                                      i * grayscale_fraction,
                                      i * grayscale_fraction)
                                  for i in range(
                    self.user_settings.num_edges + 1)}

    def generate_cells(self):
        for i in range(self.game_data.num_hor_cells):
            cell_row = []
            for j in range(self.game_data.num_ver_cells):
                cell_row.append(
                    Cell(
                        screen=self.game_data.screen,
                        x_pos=i * self.game_data.cell_width +
                        self.game_data.left_border_width,
                        y_pos=j * self.game_data.cell_height +
                        self.game_data.top_border_width,
                        row=j, col=i, cell_width=self.game_data.cell_width,
                        cell_height=self.game_data.cell_height
                        )
                    )
            self.game_data.cell_matrix.append(cell_row)

    def fill_cell(self, mouse_pos, fill):
        # Check if mouse click was inside cell grid
        if ((self.game_data.left_border_width < mouse_pos[0] <
            self.game_data.screen_width - self.game_data.right_border_width)
                and (self.game_data.top_border_width < mouse_pos[1] <
                     self.game_data.screen_height -
                     self.game_data.bottom_border_width)):
            x_pos = int((mouse_pos[0] - self.game_data.left_border_width) /
                        self.game_data.cell_width)
            y_pos = int((mouse_pos[1] - self.game_data.top_border_width) /
                        self.game_data.cell_height)

            if self.user_settings.thickness == "small":
                thickness_directions = [(0, 0)]
            elif self.user_settings.thickness == "medium":
                thickness_directions = [(0, 0), (1, 0), (0, 1), (1, 1)]
            elif self.user_settings.thickness == "large":
                thickness_directions = [(0, 0), (-1, 0), (1, 0), (0, -1),
                                        (0, 1), (-1, -1), (1, 1), (-1, 1),
                                        (1, -1)]

            cells = []
            for direction in thickness_directions:
                row = x_pos + direction[0]
                col = y_pos + direction[1]
                if self.is_valid_pos(row, col):
                    cells.append(self.game_data.cell_matrix[row][col])

            for cell in cells:
                # use this to add intensity setting: add a bool to turn the
                # statement on and off. also add setting for 8 vs 4 vs 0
                # spill-over directions.
                if (fill and cell.cell_value == 1 and not
                        self.user_settings.pressure_sensitivity):
                    continue

                cell.fill(fill)
                if fill:
                    add_to_adj = 1
                else:
                    add_to_adj = -1

                if self.user_settings.num_edges == 8:
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1),
                                  (1, 1), (-1, 1), (1, -1)]
                elif self.user_settings.num_edges == 4:
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                elif self.user_settings.num_edges == 0:
                    directions = []

                for direction in directions:
                    row = cell.row + direction[0]
                    col = cell.col + direction[1]
                    if self.is_valid_pos(row, col):
                        self.set_grayscale(row, col, add_to_adj)

    def is_valid_pos(self, row, col):
        return ((0 <= row <= self.game_data.num_ver_cells - 1) and (
                0 <= col <= self.game_data.num_hor_cells - 1))

    def set_grayscale(self, row, col, add_to_adj):
        cell = self.game_data.cell_matrix[col][row]
        cell.update_adjacent_num(add_to_adj)
        if cell.cell_value != 1:
            cell.cell_value = self.value_map[cell.num_adjacent_active_cells]
            cell.cell_active_color = self.grayscale_map[
                cell.num_adjacent_active_cells]

    def fill_all_cells(self, fill):
        for row in self.game_data.cell_matrix:
            for cell in row:
                cell.fill(fill)
                cell.num_adjacent_active_cells = 0

    def display_all_cells(self):
        for row in self.game_data.cell_matrix:
            for cell in row:
                cell.draw()

    def is_empty_grid(self):
        for row in self.game_data.cell_matrix:
            for cell in row:
                if cell.cell_value != 0: return False

        return True
