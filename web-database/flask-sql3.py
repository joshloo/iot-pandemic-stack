import sqlite3
from flask import Flask, request, jsonify, render_template, send_file, make_response
from datetime import datetime
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io

app = Flask(__name__)
DATABASE = 'covid.db'

conn = sqlite3.connect(DATABASE)
    
# Get Max number of rows (table size)
def maxRowsTable():
    curs = conn.cursor()
    for row in curs.execute("select COUNT(timestamp) from  user"):
        print("xxxx" , row)
        maxNumberRows=row[0]
    print("b" , maxNumberRows)
    return maxNumberRows

# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
        numSamples = 100

def getHistData(numSamples):
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    curs.execute("SELECT * FROM user ORDER BY timestamp DESC LIMIT "+ str(numSamples))
    data = curs.fetchall()
    timestamp = []
    username = []
    ic = []
    location = []
    temperature = []
    for row in reversed(data):
        timestamp.append(row[0])
        username.append(row[1])
        ic.append(row[2])
        location.append(float(row[3]))
        temperature.append(float(row[4]))
    return timestamp, username, ic, location, temperature

@app.route('/')
def index():
    timestamp, username, ic, location, temperature = getHistData(numSamples)
    ys = temperature
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Temperature [°C]")
    axis.set_xlabel("Samples")
    axis.set_ylim(0,50)
    axis.grid(True)
    xs = range(numSamples)
    
    print(xs, xs)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print(timestamp, username, ic, location, temperature, numSamples)
    return response

if __name__ == '__main__':
    app.run(debug=True)