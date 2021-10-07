import random

Vmax = 5
P = 0.5

def key(car):
    return car.GetX()

class Car:
    def __init__(self, x):
        self._v = random.randint(0, Vmax + 1)
        self._a = 1
        self._x = x

    def CompV(self, gap):
        self._v = min(self._v + self._a, Vmax)
        self._v = min(self._v, gap - 1)
        if random.randint(0, 10) >= P * 10:
            self._v = max(self._v - 1, 0)

        return self._v

    def SetX(self, x):
        self._x = x

    def GetX(self):
        return self._x

class Line:
    def __init__(self, cells, cars):
        self._n_cells = cells
        self._n_cars = cars
        self._cars = []

    def Init(self):
        indexes = list(range(self._n_cells))

        for i in range(self._n_cars):
            index = random.choice(indexes)
            car = Car(index)
            self._cars.append(car)
            indexes.remove(index)

        self._cars.sort(key=key)

    def Comp(self):

        for i in range(self._n_cars):
            if i == self._n_cars - 1:
                gap = 10
            else:
                gap = self._cars[i + 1].GetX() - self._cars[i].GetX()

            v = self._cars[i].CompV(gap)

            if self._cars[i].GetX() + v >= self._n_cells:
                del self._cars[i]
                self._n_cars += - 1
            else:
                self._cars[i].SetX(self._cars[i].GetX() + v)

    def GetX(self):
        return [x.GetX() for x in self._cars]


if __name__ == "__main__":
    line = Line(50, 10)
    line.Init()
    print(line.GetX())
    while 1:
        if input():
            line.Comp()
            print(line.GetX())

