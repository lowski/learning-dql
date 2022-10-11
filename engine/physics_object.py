from .base import DrawableComponent, Positionable
from .drawable_object import DrawableCircle, DrawableObject, DrawableRectangle
from .hittable_object import HittableCircle, HittableObject, HittableRectangle


class PhysicsObject(Positionable, DrawableComponent):
    def __init__(self, hittable: HittableObject, drawable: DrawableObject):
        super().__init__()
        self.hittable = hittable
        self.drawable = drawable

    def draw(self, canvas):
        self.drawable.draw(canvas)

    @property
    def pos(self):
        return self.hittable.pos

    @pos.setter
    def pos(self, value):
        self.drawable.pos = value
        self.hittable.pos = value


class PhysicalRectangle(PhysicsObject):
    def __init__(self, width, height, color, pos=(0, 0)):
        super(PhysicalRectangle, self).__init__(HittableRectangle(width, height, pos=pos),
                                                DrawableRectangle(width, height, 0, color=color, pos=pos))


class PhysicalCircle(PhysicsObject):
    def __init__(self, radius, color='black', pos=(0, 0)):
        super(PhysicalCircle, self).__init__(HittableCircle(radius, pos=pos),
                                             DrawableCircle(radius, color=color, pos=pos))
