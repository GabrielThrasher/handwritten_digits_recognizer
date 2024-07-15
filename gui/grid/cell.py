from program_info.program_wide_imports import *


class Cell:
    def __init__(self, screen, x_pos, y_pos, row, col, cell_width, cell_height):
        self.screen = screen

        # Cell properties
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.row = row
        self.col = col
        self.cell_width = cell_width
        self.cell_height = cell_height

        self.cell_unfill_color = (0, 0, 0)
        self.cell_fill_color = (225, 225, 225)
        # cell status - 1 for filled and 0 for unfilled (nums used in ML model)
        self.cell_value = 0
        self.num_adjacent_active_cells = 0
        self.cell_active_color = self.cell_unfill_color

        # Cell border properties
        self.cell_border_color = (150, 150, 150)
        self.cell_border_layer = pg.Surface(
            (self.cell_width, self.cell_height), pg.SRCALPHA
        )
        self.cell_border_layer.set_alpha(7)

    def __str__(self):
        return f"Cell {self.x_pos} {self.y_pos}"

    def draw(self):
        # Draw cell
        pg.draw.rect(
            self.screen, self.cell_active_color,
            pg.Rect(
                self.x_pos, self.y_pos, self.cell_width,
                self.cell_height
                )
            )
        # Draw cell border
        pg.draw.rect(
            self.cell_border_layer, self.cell_border_color,
            pg.Rect(0, 0, self.cell_width, self.cell_height),
            width=1
            )
        self.screen.blit(self.cell_border_layer, (self.x_pos, self.y_pos))

    def fill(self, fill):
        if fill:
            self.cell_value = 1
            self.cell_active_color = self.cell_fill_color

        if not fill:
            self.cell_value = 0
            self.cell_active_color = self.cell_unfill_color

    def update_adjacent_num(self, addend):
        if addend > 0:
            self.num_adjacent_active_cells = min(
                4, self.num_adjacent_active_cells + addend
                )
        elif addend < 0:
            self.num_adjacent_active_cells = max(
                0, self.num_adjacent_active_cells + addend
                )
