from .CarController import CarDriver
from .PortController import PortDriver
from .LightsController import LightsController
from .Util.Consts import *


class Controller:

    @staticmethod
    def Init():
        PortDriver.setMapFromFile(NameOsmFile)  # ("test.txt")
        PortDriver.getMapIntoFile()

        CarDriver.init()
        LightsController.init()

    @staticmethod
    def Change():

        CarDriver.comp()

        PortDriver.getCarsIntoFile()

    @staticmethod
    def SetMapJson():
        PortDriver.setMapFromFile(NameMapFile)
