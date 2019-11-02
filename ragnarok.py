# from app import app
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'sfdlnsfsjs3294sldoi23oejw'
socketio = SocketIO(app)

from app import routes

if __name__ == '__main__':
    socketio.run(app)