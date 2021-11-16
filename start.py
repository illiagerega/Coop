import time
from flask import Flask, request, render_template
from Back.Model.MainController import Controller
from Front.parser import *
from Front.db import *
from Back.Model.DbController import getParams
import os
import pathlib
from werkzeug import *

# Presets' content below

received_status = False

Map_html = None
Cars_html = None

static_folder = 'Front'

# Flask's content below
app = Flask(__name__, static_folder=(static_folder + '/static'), static_url_path='', template_folder=(static_folder + "/templates"))

UPLOAD_FOLDER = os.path.abspath('Front/uploads')
ALLOWED_EXTENSIONS = set(['osm'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from flask_restful import reqparse

def parse_arg_from_requests(arg, **kwargs):
    parse = reqparse.RequestParser()
    parse.add_argument(arg, **kwargs)
    args = parse.parse_args()
    return args[arg]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    #map = parser.datamap()
    #data = parser.data()
    #return render_template('index.html', data=data, map=map)
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            value = request.form.get('value')

            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            db.changeParams(file_path, value)
            return render_template('settings.html')
    
    else:

        return render_template('settings.html')

@app.route('/choose')
def choose():
    return render_template('choose.html')

@app.route('/2d', methods=['GET', 'POST'])
def type1():
    # map = parser.datamap()
    # data = parser.data()

    global received_status

    received_status = False
    html = ''

    if request.method == 'GET':
        operation = parse_arg_from_requests('operation')

        if operation == None:
            # print(request.form)
            return render_template('2d.html', data=html)

        
        if operation == "setMap":
            data = getParams()
            Controller.init(str(pathlib.Path(__file__).parent.resolve()) + data[1], data[2])

            html = decodeMap(Controller.Map)



        elif operation == "setCars":

            html = Cars_html

        else:
            pass
            
            
    
    received_status = False

    return render_template('2d.html', map = html)

@app.route('/3d')
def type2():
    return render_template('3d.html')

def setCars(channel, method_frame, header_frame, body):
    global received_status, Cars_html

    if not received_status:
        # Rabbit.sendData('setCars', 'control')
        
        Cars_html = parser.decodeCars(body)
        received_status = True

def setMap(channel, method_frame, header_frame, body):
    global received_status, Map_html


    if not received_status:
        
        Map_html = parser.decodeMap(body)
        received_status = True

if __name__ == "__main__":
    app.run(debug=True)
    
    # Rabbit.declareFunc('map', setMap)
    # Rabbit.declareFunc('cars', setCars)
    # Rabbit.startConsuming()




# from Back.Model.MainController import Controller
# import Back.Model.MessageController
# import socket, time
# from subprocess import call
# from json import load
# import threading
# import os
# import pathlib
# import Back.Model.DbController as db
# from Front.main import runServer


# data = db.getParams()

# paused = False

# # def _settingCars():
# #     global paused

# #     while True:
# #         if paused == False:
# #             Controller.change()
# #         # time.sleep(speed) # speed of simulation


# def main():
#     print('set')

#     # Controller.setMap(str(pathlib.Path(__file__).parent.resolve()) + data[1])
#     Controller.init(int(data[2]))

#     time.sleep(0.5)
#     sim_thread = threading.Thread(target=runServer, args=())
#     sim_thread.daemon = False
#     is_paused = False
#     stop_sim = False

#     sim_thread.start()

#     print("setting is end")

# if __name__ == "__main__":
#     main()