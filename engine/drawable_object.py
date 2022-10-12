import tkinter

from .base import DrawableComponent, Positionable


class DrawableObject(Positionable, DrawableComponent):
    def __init__(self, color='black', pos=(0, 0)):
        super().__init__()
        self.color = color
        self.pos = pos

    def draw(self, canvas):
        raise NotImplementedError('Not Implemented')


class DrawableCircle(DrawableObject):
    def __init__(self, radius, color='black', pos=(0, 0)):
        super().__init__(color, pos)
        self.radius = radius

    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius,
                           fill=self.color)


class DrawableRectangle(DrawableObject):
    def __init__(self, width, height, rotation, color='black', pos=(0, 0)):
        super().__init__(color, pos)
        self.width = width
        self.height = height
        self.rotation = rotation

    def draw(self, canvas):
        canvas.create_rectangle(self.x - self.width / 2, self.y - self.height / 2,
                                self.x + self.width / 2, self.y + self.height / 2,
                                fill=self.color)


class DrawableLine(DrawableObject):
    def __init__(self, start, end, color='black'):
        super().__init__(color, start)
        self.end = end

    def draw(self, canvas):
        canvas.create_line(
            self.x, self.y, self.end[0], self.end[1], fill=self.color)
