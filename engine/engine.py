import time
import tkinter as tk
from time import sleep
from typing import Union

from .base import DrawableComponent, UpdatableComponent


class Engine:
    def __init__(self, target_fps=60):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=500, height=500)
        self.canvas.pack()
        self.objects = []
        self.target_fps = target_fps

    def add(self, o: Union[object, list]):
        if isinstance(o, list):
            for obj in o:
                self.add(obj)
        elif o not in self.objects:
            self.objects.append(o)

    def mainloop(self):
        while True:
            frame_start = time.time()
            self.clear()

            self.update_objects()
            self.draw_objects()

            self.update()

            frame_time = time.time() - frame_start
            sleep_time = 1 / self.target_fps - frame_time
            if sleep_time > 0:
                sleep(sleep_time)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def draw_objects(self):
        for obj in self.objects:
            if isinstance(obj, DrawableComponent):
                obj.draw(self.canvas)

    def update_objects(self):
        for obj in self.objects:
            if isinstance(obj, UpdatableComponent):
                obj.update()

    def clear(self):
        self.canvas.delete('all')

    def update(self):
        self.window.update()
