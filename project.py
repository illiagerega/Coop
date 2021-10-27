from Model.MainController import Controller
import socket, time
from subprocess import call
from json import load
import threading
import os

settings_path = "/settings.json"
with open(os.getcwd() + settings_path, 'r') as file:
    settings = load(file)
    file.close()


address = settings["host_main"]
port = settings["port_main"]

class SocketDriver:
    def __init__(self):
        self.socket_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_main.connect((address, port))
        self._kill = False
        self.thread = threading.Thread(target=self._listen, args=())
        self.thread.daemon = True
        self.thread.start()

    def _decode(self, data):
        data = data.decode().split('#') # separate by '#'. The first part is a command,
                                        # the another one is data

        if data[0] == "setMap":
            Controller.setMap(data[1])


        if data[0] == "init":
            Controller.init()

        self.send(data[0])

    def _listen(self):
        print("Connected by")
        while True:
            if self._kill:
                break
            data = self.socket_main.recv(settings["buf_size"])
            self._decode(data)



    def end(self):
        self.send("quit")
        self._kill = True
        self.socket_main.close()


    def send(self, command):
        command = command.encode()
        self.socket_main.send(command)

def calling():
    call(["node", settings["server_path"]])

def decode(string, MainSocket):
    if string == "quit":
        MainSocket.end()
        return 1
    if string == "setMap":
        MainSocket.send("setMap")
    if string == "set":
        Controller.setMap("data/map_big.osm")
        Controller.init()
        print("setting is end")
    if string == "getCars":
        Controller.change()
        MainSocket.send("setCars")

def main():
    thread = threading.Thread(target=calling, args=())
    thread.daemon = True
    thread.start()
    time.sleep(5)
    MainSocket = SocketDriver()

    MainSocket.send("ready")
    while True:
        command = str(input())
        if decode(command, MainSocket):
            break



if __name__ == "__main__":
    main()


