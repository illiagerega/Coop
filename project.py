from Model.MainController import Controller
import socket, time
from subprocess import call
from json import load
import threading

settings_path = "settings.json"
with open(settings_path, 'r') as file:
    settings = load(file)
    file.close()


address = settings["host_main"]
port = settings["port_main"]

class SocketDriver:
    def __init__(self):
        self.socket_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_main.connect((address, port))
        self.thread = threading.Thread(target=self._listen, args=())
        self.thread.daemon = True
        self.thread.start()

    def _decode(self, string):
        return string

    def _listen(self):
        print("Connected by")
        while True:
            data = self.socket_main.recv(settings["buf_size"])
            if not data:
                break

    def end(self):
        self.socket_main.close()



    def send(self, command):
        command = command.encode()
        self._conn.sendall(command)

def calling():
    call(["node", settings["server_path"]])

def main():
    thread = threading.Thread(target=calling, args=())
    thread.daemon = True
    thread.start()
    time.sleep(5)
    MainSocket = SocketDriver()




if __name__ == "__main__":
    main()


