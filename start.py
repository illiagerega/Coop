import time
from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
from werkzeug.utils import redirect
from Back.Model.CarController import CarDriver
from Back.Model.MainController import Controller
from Front.parser import *
from Front.db import Settings
from Back.Model.DbController import getParams
from Back.Model.PortController import PortDriver
import os
import pathlib
from werkzeug import *
import json
# Hell

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

html = ''

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

            Settings.changeParams(file_path, value)
            return render_template('settings.html')
    
    else:

        return render_template('settings.html')

@app.route('/choose')
def choose():
    return render_template('choose.html')

@app.route('/2d', methods=['GET', 'POST'])
def type1():

    data = getParams()
    Controller.init(data[1], data[2])
    map_ = Controller.Map

    data = PortDriver.getCarsIntoFile()
    cars_ = json.loads(data)

    lights = PortDriver.getLightsIntoFile()
    

    return render_template('2d.html', map = html, map_ = map_, cars_ = cars_, lights = lights)

@app.route('/map', methods=['GET', 'POST'])
def info():

    global html

    if request.method == 'GET':
        operation = parse_arg_from_requests('operation')

        if operation == None:
            # print(request.form)
            return render_template('2d.html', data=html)

        

        if operation == "setMap":
            

            data = getParams()
            Controller.init(data[1], data[2])

        
            html = decodeMap(Controller.Map)
            # print(html)
            return html


        elif operation == "setCars":
            Controller.change()
            html_ = decodeCars(PortDriver.getCarsIntoFile())
            html_ += decodeLights(PortDriver.getLightsIntoFile())            
            return html_


        else:
            pass

@app.route('/3d')
def type2():
    return render_template('3d.html')

@app.route('/editior', methods=['GET', 'POST'])
def editior():
    if request.method == 'POST':
        value = request.form.get('data')
        print(value)
        return redirect('/2d')

if __name__ == "__main__":
    app.run(debug=True)
 
 