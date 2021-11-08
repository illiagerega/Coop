from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/settings', methods=['POST'])
def my_form_post():
    ncars = request.form['cars_n']
    map = request.form['item']
    if request.method == 'POST':
       with open('nopol.txt', 'w') as f:
            f.write(f'{ncars}, {map}')
    return render_template('settings.html', nopol=ncars)

@app.route('/model')
def model():
    return render_template('model.html')

if __name__ == "__main__":
    app.run(debug=True)