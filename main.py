#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request, flash, session
#from flask.ext.session import Session
from flask_sqlalchemy import SQLAlchemy
import RPi.GPIO as GPIO
from datetime import datetime , time
#from classes import CurrentPlant, PlantPreset, Brightness, Humidity

#GPIO 8 = lampka testowa
#GPIO 11 = sensor wilgoci
#GPIO 13 = lampa lewa
#GPIO 15 = lampa prawa
#GPIO 16 = wlacznik pompy

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(8, GPIO.OUT)
GPIO.output(8, False)
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, False)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, False)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, False)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class CurrentPlant(db.Model):
    __tablename__ = 'currentPlant'
    id = db.Column(db.Integer, primary_key=True)
    LastWatering = db.Column(db.DateTime, nullable=True)
    LastIrradiation = db.Column(db.DateTime, nullable=True)
    plantPreset = db.Column(db.Integer, db.ForeignKey('plantPreset.id'), nullable=False)
    
class PlantPreset(db.Model):
    __tablename__ = 'plantPreset'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    lampFrom = db.Column(db.Time, nullable=True)
    lampTo = db.Column(db.Time, nullable=True)
    wateringDays = db.Column(db.Integer, nullable=True)
    brightnessID = db.Column(db.Integer, db.ForeignKey('brightness.id'), nullable=True)
    humidityID = db.Column(db.Integer, db.ForeignKey('humidity.id'), nullable=True)
    
        
class Brightness(db.Model):
    __tablename__ = 'brightness'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    brightness = db.Column(db.Integer, nullable=False)
    
class Humidity(db.Model):
    __tablename__ = 'humidity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    soilHumidity = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    state = GPIO.input(8)
    CP = CurrentPlant.query.first()
    return render_template('index.html' , pumpStatus = state , lastWatering=CP.LastWatering , lampStatus=0 , lastIrradiation = CP.LastIrradiation)

@app.route('/addPreset', methods=['GET', 'POST'])
def addPreset():
    GPIO.output(8, False)
    humidityOptions = Humidity.query.all()
    brightnessOptions = Brightness.query.all()
    return render_template('addPreset.html' , wateringOptions = humidityOptions , lightOptions = brightnessOptions )

@app.route('/addPresetDataHandle', methods=['GET', 'POST'])
def addPresetDataHandle():
    if request.method == 'POST':
        name = request.form['name']
        lampFrom = request.form['from'].split(":")
        lampTo = request.form['to'].split(":")
        lampFrom = time(hour=int(lampFrom[0]), minute = int(lampFrom[1]))
        lampTo = time(hour=int(lampTo[0]), minute = int(lampTo[1]))
        wateringDays = request.form['daysCount']
        brightnessID = request.form['ilumnatingType']
        humidityID = request.form['wateringType']
        newPlant = PlantPreset(name = name,lampFrom = lampFrom , lampTo = lampTo , wateringDays = wateringDays , brightnessID = brightnessID , humidityID = humidityID)
        db.session.add(newPlant)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('addPreset'))

@app.route('/changePlantSettings')
def changePlantSettings():
    plantSettings = PlantPreset.query.all()
    return render_template('chosePreset.html' , options = plantSettings )

@app.route('/changePlantSettingsHandler')
def changePlantSettingsHandler():
    plant = CurrentPlant.query.first()
    plant.plantPreset = 1
    session.commit()
    return redirect(url_for('index'))

@app.route('/test',methods = ["POST"])
def test():
    flash("flash test")
    return render_template('test.html')

@app.route('/testHandler', methods=['GET', 'POST'])
def testHandler():
    if request.method == 'POST':
        error = None
        return redirect(url_for('test'))
        #try:
        #   flash(request.form['testText'])
        #   return render_template('testout.html' , error = error )
    else:
        return redirect(url_for('test'))

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'
    #sess = Session()
    #sess.init_app(app)
    app.run(host='0.0.0.0', port= 8080 , debug = True)
