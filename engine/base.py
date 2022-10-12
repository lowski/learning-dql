import tkinter
from typing import TYPE_CHECKING, Tuple, Union

if TYPE_CHECKING:
    from engine.engine import Engine


class Component:
    def __init__(self):
        self.engine: Union[Engine, None] = None

    def added(self, engine):
        pass


class Positionable:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def pos(self) -> Tuple[float, float]:
        return self.x, self.y

    @pos.setter
    def pos(self, value: Tuple[float, float]):
        self.x, self.y = value

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Positionable({self.x}, {self.y})"


class DrawableComponent(Component):
    def draw(self, canvas: tkinter.Canvas):
        raise NotImplementedError("Not implemented")


class UpdatableComponent(Component):
    def update(self):
        raise NotImplementedError("Not implemented")
