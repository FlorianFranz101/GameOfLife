import numpy as np
import pygame


class Game:
    # define colors for simulation
    col_about_to_die = (200, 200, 225)
    col_alive = (255, 255, 215)
    col_background = (10, 10, 40)
    col_grid = (30, 30, 60)

    def __init__(self, ctrl):
        self.init(ctrl)

    def update(self):
        self.sync_size_and_cells()
        sizex = self.ctrl.cellsx
        sizey = self.ctrl.cellsy
        # start with a bunch of dead cells (alive = 1, dead=0)
        nxt = np.zeros((sizey, sizex))

        for r, c in np.ndindex((sizey, sizex)):
            rm1mod = (r - 1) % sizey
            cm1mod = (c - 1) % sizex
            r1mod = (r + 1) % sizey
            c1mod = (c + 1) % sizex
            num_alive = self.cells[r, cm1mod] + self.cells[rm1mod, c] + self.cells[rm1mod, cm1mod] + self.cells[
                r1mod, c1mod] + self.cells[r1mod, c] + self.cells[r1mod, cm1mod] + self.cells[r, c1mod] + self.cells[
                            rm1mod, c1mod]
            if (self.cells[r, c] == 1 and 2 <= num_alive <= 3) or (self.cells[r, c] == 0 and num_alive == 3):
                nxt[r, c] = 1
        self.cells = nxt

    def draw_board(self, surface, sz):
        self.sync_size_and_cells()
        # fill with grid color
        surface.fill(self.col_grid)
        for r, c in np.ndindex((self.ctrl.cellsy, self.ctrl.cellsx)):
            if self.cells[r, c] == 1:
                # set color of cell about to die
                col = self.col_alive
            col = col if self.cells[r, c] == 1 else self.col_background
            pygame.draw.rect(surface, col, (c * sz, r * sz, sz - 1, sz - 1))

    def flip_cell(self, x, y):
        if self.ctrl.cellsx < x + 1 or self.ctrl.cellsy < y + 1:
            return
        if self.cells[y, x] == 0:
            self.cells[y, x] = 1
        else:
            self.cells[y, x] = 0

    def init(self, ctrl):
        self.ctrl = ctrl
        self.cells = np.zeros((ctrl.cellsy, ctrl.cellsx))
        pattern = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 1, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 1, 1, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0]]);
        pos = (3, 3)
        self.cells[pos[0]:pos[0] + pattern.shape[0], pos[1]:pos[1] + pattern.shape[1]] = pattern

    def sync_size_and_cells(self):
        y, x = self.cells.shape
        if x >= self.ctrl.cellsx and y >= self.ctrl.cellsy:
            return
        shape = np.shape(self.cells)
        padded_array = np.zeros((self.ctrl.cellsy, self.ctrl.cellsx))
        padded_array[:shape[0], :shape[1]] = self.cells
        self.cells = padded_array
        print(padded_array)
