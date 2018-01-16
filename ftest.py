from flask import *

app = Flask(__name__)

@app.route('/')
def test():
    return render_template('index.html')

@app.route('/other')
def other():
    return 'weird'
