#!/usr/bin/env python
from flask import Flask, render_template
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#GPIO.setup(8, GPIO.OUT)
#GPIO.output(8, False)

app = Flask(__name__)

temp = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lamp')
def lamp():
    #GPIO.output(8, True)
    return render_template('lamp.html')

@app.route('/pump')
def pump():
    #GPIO.output(8, False)
    return render_template('pump.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080 , debug = True)
