import gameloop
import threading
import time
from os import listdir
from os.path import isfile, join
from video_export import VideoExport
from rle_converter import read_board_from_string
import matplotlib.pyplot as plt
from pathlib import Path
import pygame
import sys
import numpy
import os
# start single cpu benchmark no video
def benchmark(gameloop, iterations, patterns, threads, gpu):
    print("benchmark started")
    times = [[], []]
    gameloop.ctrl.threads = threads
    gameloop.ctrl.gpu = gpu
    for pattern in patterns:
        gameloop.ctrl.current_pattern = pattern.replace(".rle", "")
        import_pattern(gameloop, pattern)
        start = time.time()
        for i in range(iterations):
            gameloop.game.update()
        total = time.time() - start
        average_per_iteration = total / iterations
        times[0].append(total)
        times[1].append(average_per_iteration)
        print("benchmark done")

    return times


def benchmark_video(gameloop, iterations, patterns, threads, gpu):
    print("benchmark started")
    times = [[], []]
    gameloop.ctrl.threads = threads
    gameloop.ctrl.gpu = gpu
    gameloop.ctrl.export_timesteps = iterations
    for pattern in patterns:
        gameloop.ctrl.current_pattern = pattern.replace(".rle", "")
        import_pattern(gameloop, pattern)
        start = time.time()
        export = VideoExport(game=gameloop.game, ctrl=gameloop.ctrl, gameloop=gameloop)
        export.export()
        while gameloop.ctrl.export_running: pass
        total = time.time() - start
        average_per_iteration = total / iterations
        times[0].append(total)
        times[1].append(average_per_iteration)
    print("benchmark done")
    return times


def import_pattern(gameloop, pattern):
    print("file", pattern)
    with open("patterns/" + pattern, 'r') as file:
        importtext = file.read()
    cells = read_board_from_string(importtext)
    gameloop.ctrl.cellsx = cells.shape[1]
    gameloop.ctrl.cellsy = cells.shape[0]
    gameloop.game.cells = cells

def plot_and_save(times, patterns, name):
    print("plotting")
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    ax.bar(patterns,times[0])
    plt.plot()
    save_csv(times, patterns, name)
    fig.savefig("benchmarking/"+name+'.png')
def save_csv(times, patterns, name):
    out = ""
    for a in times:
        out =out + str(a)+","
    out = out +"\n"
    for a in patterns:
        out =out +a+","
    with open("benchmarking/"+name+'.csv', "w") as text_file:
        text_file.write(out)

if not os.path.exists('benchmarking'):
    os.makedirs('benchmarking')
iterations = 100
max_patterns = 10
gameloop = gameloop.GameLoop()
thread = threading.Thread(target=gameloop.main)
thread.start()
# wait for game initializing
time.sleep(1)
patterns = [f for f in listdir("patterns") if isfile(join("patterns", f))][0:10]

single = benchmark(gameloop, iterations, patterns, 1, False)
single_video = benchmark_video(gameloop, iterations, patterns, 1, False)
plot_and_save(single, patterns, "One CPU")
plot_and_save(single_video, patterns, "One CPU Video Export")
multi = benchmark(gameloop, iterations, patterns, 4, False)
multi_video = benchmark_video(gameloop, iterations, patterns, 4, False)
plot_and_save(multi, patterns, "Multiple threads CPU")
plot_and_save(multi_video, patterns, "Multiple threads CPU Video Export")
gpu = benchmark(gameloop, iterations, patterns, 0, True)
gpu_video = benchmark_video(gameloop, iterations, patterns, 0, True)
plot_and_save(gpu, patterns, "GPU")
plot_and_save(gpu_video, patterns, "GPU Video Export")
os._exit(0)