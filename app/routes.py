# from app import app
from flask import Flask, jsonify
import random

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def home():
    return jsonify(response='The Ragnarök is coming ...')


@app.route('/mashtun', methods=['GET'])
@app.route('/mashtun/get/temperature', methods=['GET'])
def getMashTunTemperature():
    return jsonify(temperature=random.randrange(0, 100))


@app.route('/mashtun/set/temperature/<int:degrees>', methods=['POST'])
def setMashTunTemperature(degrees):
    return str(degrees)