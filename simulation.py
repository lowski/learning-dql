from engine.engine import Engine
from engine.physics_object import PhysicalCircle


def main():
    engine = Engine()
    engine.add_object(PhysicalCircle(10, color='red', pos=(100, 100)))

    engine.mainloop()


if __name__ == "__main__":
    main()
