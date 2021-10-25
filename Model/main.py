from Util.MapController import Map
from CarController import CarDriver
from LightsController import LightsController
from PortController import PortDriver
from Util.SimulationShrimp import sim
from Util.Consts import *

def main():
    #Map.init("test.txt")
    #Map.getEverythingIntoFile()
    PortDriver.setMapFromFile(NameOsmFile)  #("test.txt")
    PortDriver.getMapIntoFile()

    CarDriver.init()
    LightsController.init()

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

        sim(CarDriver)
        CarDriver.comp()
        print()
        print()

        PortDriver.getCarsIntoFile()

if __name__ == "__main__":
    main()
