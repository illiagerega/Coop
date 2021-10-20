from Util.MapController import Map
from CarController import CarDriver


def main():
    Map.init("test.txt")

    CarDriver.init()
    for node in CarDriver.cars_array[0].way:
        print(node)

    print()
    print()
    print("Simulation: ")
    print()
    print()
    for i in range(20):

        for car in CarDriver.cars_array:
            print(car.x)
            print(car.getLines()[car.currentLine])
            print(car.getCoordinates())

        CarDriver.comp()
        print()
        print()
if __name__ == "__main__":
    main()
