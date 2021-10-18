import random

Acceleration = 1
StartVelocity = 0
MaxVelocity = 3
Probability = 0.5  # for city - 0.5; for highway - 0.3


class Car:
    def __init__(self, x, ax=None, ay=None):
        self._v = StartVelocity
        self._a = Acceleration
        self.pause = 0
        self.x = x
        self.apos = (ax, ay)
        self.way = []
        self.pos = (None, None)



    def CompV(self, gap):
        self._v = min(self._v + self._a, MaxVelocity)
        self._v = min(self._v, gap - 1)
        if random.randint(0, 10) >= Probability * 10:
            self._v = max(self._v - 1, 0)

        return self._v + self.x