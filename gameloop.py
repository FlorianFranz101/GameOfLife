import pygame
import pygame_gui
import numpy as np
import time
from ui_elements import UIElements as UI
from game import Game
from control import Controls as Ctrl
import math
import sys
from rle_converter import read_board_from_string

class GameLoop:

    def main(self):
        pygame.init()
        self.ctrl = Ctrl()
        with open("patterns/default.rle", 'r') as file:
            importtext = file.read()
        cells = read_board_from_string(importtext)
        self.game = Game(self.ctrl, cells)
        self.ui = UI(self.game, self.ctrl, self)
        # calculate window size by amount of cells * cell size
        self.surface = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
        self.manager = pygame_gui.UIManager((1600, 900))
        self.cellsize = self.get_cell_size(1600, 900, self.ctrl.cellsx, self.ctrl.cellsy)
        self.ui.define_elements(self.manager)

        pygame.display.set_caption("Game of Life")
        clock = pygame.time.Clock()
        time_since_update = 0
        # Game loop
        while True:

            time_delta = clock.tick(60) / 1000.0
            time_since_update = time_since_update + time_delta
            if not self.ctrl.is_paused and not self.ctrl.export_running:
                if time_since_update > self.ctrl.ticktime:
                    self.game.update()
                    time_since_update = 0
                # calculate and change cell viewmodel

            # if user wants to exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                # flip cell
                if event.type == pygame.MOUSEBUTTONUP:
                    if(self.ctrl.celledit):
                        x, y = pygame.mouse.get_pos()
                        self.game.flip_cell(int(x / self.cellsize), int(y / self.cellsize))

                if event.type == pygame.VIDEORESIZE:
                    # There's some code to add back window content here.
                    self.surface = pygame.display.set_mode((event.w, event.h),
                                                           pygame.RESIZABLE)
                    self.manager.set_window_resolution((event.w, event.h))
                    self.cellsize = self.get_cell_size(event.w, event.h, self.ctrl.cellsx, self.ctrl.cellsy)
                self.ui.handle_event(event)
                self.manager.process_events(event)
            if self.ctrl.cellschanged:
                self.ctrl.cellschanged = False
                self.cellsize = self.get_cell_size(self.surface.get_size()[0], self.surface.get_size()[1],
                                                   self.ctrl.cellsx, self.ctrl.cellsy)
            self.ui.update()
            if not self.ctrl.export_running: self.game.draw_board(self.surface, self.cellsize)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.surface)
            # update view
            pygame.display.update()

    def get_cell_size(self, windowx, windowy, cellsx, cellsy):
        return min(windowx / cellsx, windowy / cellsy)

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    GameLoop().main()
