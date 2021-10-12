from Util.MapController import Map
from CarController import CarDriver


def main():
    Map.init("test.txt")

    CarDriver.init()
    print(CarDriver.cars_array[0].way)


if __name__ == "__main__":
    main()
