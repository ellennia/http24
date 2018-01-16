from flask import *

app = Flask(__name__)

@app.route('/')
def test():
    return '<center><h1><i>Hi people!</i></h1></center>'

@app.route('/other')
def other():
    return 'weird'
