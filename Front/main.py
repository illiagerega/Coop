from flask import *
import parser
import db
import os
from werkzeug import *

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath('uploads')
ALLOWED_EXTENSIONS = set(['osm'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
def chooose():
    return render_template('choose.html')

@app.route('/2d')
def type1():
    map = parser.datamap()
    data = parser.data()
    return render_template('2d.html', data=data, map=map)

@app.route('/3d')
def type2():
    return render_template('3d.html')

if __name__ == "__main__":
    app.run(debug=True)