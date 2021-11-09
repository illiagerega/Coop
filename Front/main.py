from flask import Flask, render_template, request, send_from_directory
import parser

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    data = parser.data()
    map = parser.datamap()
    return render_template('index.html', data=data, map=map)


if __name__ == "__main__":
    app.run(debug=True)