import tkinter
import typing


class Positionable:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value: typing.Tuple[float, float]):
        self.x, self.y = value

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Positionable({self.x}, {self.y})"


class DrawableComponent:
    def draw(self, canvas: tkinter.Canvas):
        raise NotImplementedError("Not implemented")


class UpdatableComponent:
    def update(self):
        raise NotImplementedError("Not implemented")
