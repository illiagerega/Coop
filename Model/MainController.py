from .CarController import CarDriver
from .PortController import PortDriver
from .LightsController import LightsController
from .Util.MapController import Map
from .Util.Consts import *


class Controller:

    @staticmethod
    def setMap(Name):
        if ',' in Name:
            PortDriver.setMapByName(Name)
        else:
            PortDriver.setMapFromFile(Name)


    @staticmethod
    def init():
        #PortDriver.setMapFromFile(NameOsmFile)  # ("test.txt")

        PortDriver.getMapIntoFile()

        Map.init()
        CarDriver.init()
        LightsController.init()

    @staticmethod
    def change():

        CarDriver.comp()

        PortDriver.getCarsIntoFile()

    @staticmethod
    def setMapJson():
        PortDriver.setMapFromFile(NameMapFile)
