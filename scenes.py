from engine.physics_object import PhysicalRectangle
from learning.scene import Scene

simple_corridor = Scene(
    borders=[
        PhysicalRectangle(500, 10, color='black', pos=(250, 150)),
        PhysicalRectangle(500, 10, color='black', pos=(250, 350)),
        PhysicalRectangle(10, 210, color='black', pos=(5, 250)),
        PhysicalRectangle(10, 210, color='black', pos=(495, 250)),
    ],
    goals=[
        PhysicalRectangle(2, 210, color='yellow', pos=(75, 250)),
        PhysicalRectangle(2, 210, color='yellow', pos=(150, 250)),
        PhysicalRectangle(2, 210, color='yellow', pos=(225, 250)),
        PhysicalRectangle(2, 210, color='yellow', pos=(300, 250)),
        PhysicalRectangle(2, 210, color='yellow', pos=(375, 250)),
        PhysicalRectangle(2, 210, color='yellow', pos=(450, 250)),
    ],
    starting_pos=(25, 250),
    num_rays=2,
)
