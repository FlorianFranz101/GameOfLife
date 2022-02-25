import png
import cv2
import os
import time
import numpy as np
class VideoExport:
    def __init__(self, game, ctrl, gameloop):
        self.game = game
        self.ctrl = ctrl
        self.gameloop = gameloop
        self.hexalive = ctrl.export_alive_color
        self.hexdead = ctrl.export_dead_color
        self.fps = ctrl.export_fps
        self.requiredsteps = ctrl.export_timesteps

    def export(self):
        self.ctrl.export_running = True
        stepstaken = 0
        time_start = time.time()

        times= []
        max_times =10
        self.export_image(self.game.cells, "img" + str(stepstaken))
        while (not self.ctrl.abort_export) and self.requiredsteps > stepstaken:
            self.game.update()
            self.export_image(self.game.cells, "img" + str(stepstaken+1))
            stepstaken += 1
            self.ctrl.export_progress = stepstaken/self.requiredsteps
            times.append(time.time()-time_start)
            time_start = time.time()
            if(len(times)>max_times):
                times.pop(0)
            self.ctrl.estimated_time = (self.requiredsteps-stepstaken)*np.average(times)

        self.video_from_images()
        self.ctrl.export_running = False

    def export_image(self, gameboard, filename):
        height = len(gameboard)
        width = len(gameboard[0])
        img = []
        deadcolor = self.hex_string_to_tuple(self.hexdead)
        alivecolor = self.hex_string_to_tuple(self.hexalive)
        for y in range(height):
            row = ()
            for x in range(width):
                if gameboard[y][x] == 1:
                    row = row + alivecolor
                else:
                    row = row + deadcolor
            img.append(row)
        with open('images/' + filename + '.png', 'wb') as f:
            w = png.Writer(width, height, greyscale=False)
            w.write(f, img)

    def video_from_images(self):

        image_folder = 'images'
        video_name = 'videos/video.avi'

        images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, self.fps, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()

    def hex_string_to_tuple(self, hexstring):
        return (int(hexstring.replace("#", "")[0:2], 16), int(hexstring.replace("#", "")[2:4], 16),
                int(hexstring.replace("#", "")[4:6], 16))
