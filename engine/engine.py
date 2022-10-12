import time
import tkinter as tk
from time import sleep
from typing import Union

from .base import Component, DrawableComponent, UpdatableComponent


class Engine:
    def __init__(self, target_fps=60):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=500, height=500)

        self.canvas.bind('<KeyPress>', self._on_key_down)
        self.canvas.bind('<KeyRelease>', self._on_key_up)

        self.canvas.pack()
        self.canvas.focus_set()

        self.objects = []
        self.target_fps = target_fps
        self._pressed_keys = set()
        self._stop = False

    def add(self, o: Union[object, list]):
        if isinstance(o, list):
            for obj in o:
                self.add(obj)
        elif o not in self.objects:
            if isinstance(o, Component):
                o.engine = self
                o.added(self)
            self.objects.append(o)

    def start(self):
        while not self._stop:
            frame_start = time.time()
            self.clear()

            self.update_objects()
            self.draw_objects()

            self.update()

            frame_time = time.time() - frame_start
            sleep_time = 1 / self.target_fps - frame_time
            if sleep_time > 0:
                sleep(sleep_time)
        try:
            self.window.destroy()
        except Exception as _:
            pass

    def stop(self):
        self._stop = True

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

    def _on_key_down(self, event):
        self._pressed_keys.add(event.keysym)

    def _on_key_up(self, event):
        self._pressed_keys.remove(event.keysym)

    def is_key_pressed(self, key):
        return key in self._pressed_keys
