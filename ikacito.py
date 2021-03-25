class Cosa:
    def __init__(self, que_soy=""):
        print("Soy una cosa!", que_soy)


class Animal(Cosa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("GATO")
        self.dos = 2

class Robot(Cosa):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dos = 3
        print("Robot! owo")


class GatoRobot(Robot, Animal):
    def __init__(self):
        super().__init__(que_soy="gato robot")
        # Animal.__init__(self)
        # Robot.__init__(self)


g = GatoRobot()
print(g.__dict__)
