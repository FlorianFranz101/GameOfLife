import numpy as np
import pygame
import threading
import time
from numba import cuda
import math
@cuda.jit
def do_update_gpu( before, results, sizex, sizey):
    r, c = cuda.grid(2)
    if(r>= sizey or c >=sizex):
        return
    rm1mod = (r - 1) % sizey
    cm1mod = (c - 1) % sizex
    r1mod = (r + 1) % sizey
    c1mod = (c + 1) % sizex
    num_alive = before[r, cm1mod] + before[rm1mod, c] + before[rm1mod, cm1mod] + before[
        r1mod, c1mod] + before[r1mod, c] + before[r1mod, cm1mod] + before[r, c1mod] + \
                before[
                    rm1mod, c1mod]
    if (before[r, c] == 1 and 2 <= num_alive <= 3) or (before[r, c] == 0 and num_alive == 3):
        results[r, c] = 1
class Game:
    # define colors for simulation
    col_about_to_die = (200, 200, 225)
    col_alive = (255, 255, 215)
    col_background = (10, 10, 40)
    col_grid = (30, 30, 60)

    def __init__(self, ctrl, pattern):
        self.init(ctrl, pattern)

    def update(self):
        self.sync_size_and_cells()
        if (self.ctrl.gpu):
            gpuAvailable = True
            try:
                a = cuda.gpus
            except:
                print("there is no CUDA Device")
                self.ctrl.gpu = False
                self.update_single()
                gpuAvailable = False
            if gpuAvailable:
                self.update_gpu()
            return
        if (self.ctrl.threads == 1):
            self.update_single()
            return
        if (self.ctrl.threads > 1):
            self.update_multicore(self.ctrl.threads)

    def update_single(self):
        # columns
        sizex = self.ctrl.cellsx
        # row
        sizey = self.ctrl.cellsy
        # start with a bunch of dead cells (alive = 1, dead=0)
        nxt = np.zeros((sizey, sizex))
        for r, c in np.ndindex((sizey, sizex)):
            rm1mod = (r - 1) % sizey
            cm1mod = (c - 1) % sizex
            r1mod = (r + 1) % sizey
            c1mod = (c + 1) % sizex
            num_alive = self.cells[r, cm1mod] + self.cells[rm1mod, c] +\
                        self.cells[rm1mod, cm1mod] + self.cells[r1mod, c1mod] +\
                        self.cells[r1mod, c] + self.cells[r1mod, cm1mod] +\
                        self.cells[r, c1mod] + self.cells[rm1mod, c1mod]
            if (self.cells[r, c] == 1 and 2 <= num_alive <= 3) \
                    or (self.cells[r, c] == 0 and num_alive == 3):
                nxt[r, c] = 1
        self.cells = nxt

    def update_multicore(self, threads):
        sizex = self.ctrl.cellsx
        sizey = self.ctrl.cellsy
        threadList = []
        unfitted = sizey % threads
        end = 0
        results = np.zeros((sizey, sizex))
        for i in range(threads):
            prevend = end
            end = min(prevend + (sizey // threads), sizey)
            if unfitted > 0:
                end = end + 1
                unfitted = unfitted -1
            threadList.append(
                threading.Thread(target=self.do_update_multicore, args=[prevend, end, results]))
        for thread in threadList:
            thread.start()
        for i in range(len(threadList)):
            threadList[i].join()
        self.cells = results
    def do_update_multicore(self, fromy, toy, results):
        sizey = self.ctrl.cellsy
        sizex = self.ctrl.cellsx
        for r in range(fromy, toy):
            for c in range(sizex):
                rm1mod = (r - 1) % sizey
                cm1mod = (c - 1) % sizex
                r1mod = (r + 1) % sizey
                c1mod = (c + 1) % sizex
                num_alive = self.cells[r, cm1mod] + self.cells[rm1mod, c] + self.cells[rm1mod, cm1mod] + self.cells[
                    r1mod, c1mod] + self.cells[r1mod, c] + self.cells[r1mod, cm1mod] + self.cells[r, c1mod] + \
                            self.cells[
                                rm1mod, c1mod]
                if (self.cells[r, c] == 1 and 2 <= num_alive <= 3) or (self.cells[r, c] == 0 and num_alive == 3):
                    results[r, c] = 1
    def update_gpu(self):
        sizey = self.ctrl.cellsy
        sizex = self.ctrl.cellsx
        results = np.zeros((sizey, sizex))
        threadsperblock = (128, 128)
        blockspergrid_x = math.ceil(self.cells.shape[0] / threadsperblock[0])
        blockspergrid_y = math.ceil(self.cells.shape[1] / threadsperblock[1])
        blockspergrid = (blockspergrid_x, blockspergrid_y)
        do_update_gpu[threadsperblock, blockspergrid](self.cells, results, sizex, sizey)
        self.cells = results

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

    def init(self, ctrl, pattern):
        self.ctrl = ctrl
        self.cells = np.zeros((ctrl.cellsy, ctrl.cellsx))
        pos = (3, 3)
        self.cells[pos[0]:pos[0] + pattern.shape[0], pos[1]:pos[1] + pattern.shape[1]] = pattern

    def sync_size_and_cells(self):
        y, x = self.cells.shape
        if x >= self.ctrl.cellsx and y >= self.ctrl.cellsy:
            return
        print("x", self.ctrl.cellsx, "y", self.ctrl.cellsy)
        shape = np.shape(self.cells)
        padded_array = np.zeros((self.ctrl.cellsy, self.ctrl.cellsx))
        padded_array[:min(self.ctrl.cellsy,shape[0]), :min(self.ctrl.cellsx,shape[1])] = self.cells[:self.ctrl.cellsy, :self.ctrl.cellsx]
        self.cells = padded_array
