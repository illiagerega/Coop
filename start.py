from Back.Model.MainController import Controller
import Back.Model.MessageController
import socket, time
from subprocess import call
from json import load
import threading
import os
import pathlib


data = ['set', str(pathlib.Path(__file__).parent.resolve()) + '/Back/data/map_small.osm', '10']

def _settingCars():
    while True:

        Controller.change()
        time.sleep(speed) # speed of simulation


def main():
    global speed
    print('set')

    Controller.setMap(data[1])
    Controller.init(int(data[2]))

    time.sleep(0.5)
    sim_thread = threading.Thread(target=_settingCars, args=())
    sim_thread.daemon = True
    is_paused = False
    stop_sim = False

    speed = 0.75
    sim_thread.start()

    print("setting is end")

if __name__ == "__main__":
    main()
    while True:
        _settingCars()