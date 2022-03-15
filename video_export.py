import png
import cv2
import os
import time
import numpy as np
from PIL import Image
from pathlib import Path

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

        if not os.path.exists('images'):
            os.makedirs('images')
        if not os.path.exists('videos'):
            os.makedirs('videos')
        times= []
        max_times =10
        self.export_image1(self.game.cells, "img" + str(stepstaken))
        images = []
        while (not self.ctrl.abort_export) and self.requiredsteps > stepstaken:
            self.game.update()
            images.append(self.export_image1(self.game.cells, "img" + str(stepstaken+1)))
            stepstaken += 1
            self.ctrl.export_progress = stepstaken/self.requiredsteps
            times.append(time.time()-time_start)
            time_start = time.time()
            if(len(times)>max_times):
                times.pop(0)
            self.ctrl.estimated_time = (self.requiredsteps-stepstaken)*np.average(times)

        self.video_from_images(images)
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
        img = np.matrix(img)
        img = img.resize((1000, 700), 1)
        with open('images/' + filename + '.png', 'wb') as f:
            w = png.Writer(width, height, greyscale=False)
            w.write(f, img)
        return filename+".png"
    def export_image1(self, gameboard, filename):
        height = len(gameboard)
        width = len(gameboard[0])
        deadcolor = self.hex_string_to_tuple(self.hexdead)
        alivecolor = self.hex_string_to_tuple(self.hexalive)
        data = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                if gameboard[y][x] == 1:
                    data[y,x] = alivecolor
                else:
                    data[y,x] = deadcolor
        img = Image.fromarray(data,"RGB")
        if(self.ctrl.target_res_wanted):
            img = img.resize(self.get_actual_res(self.ctrl.target_res, (height, width)), resample=Image.BOX)


        img.save('images/' + filename + '.png')
        return filename+".png"
    def get_actual_res(self, desiredheight, data):
        return ( (desiredheight//data[0])*data[1], desiredheight)
    def video_from_images(self, images):
        image_folder = 'images'
        video_name = 'videos/'+self.ctrl.current_pattern
        while os.path.exists(video_name+".avi"):
            video_name = video_name +"(1)"
        video_name = video_name +".avi"
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
