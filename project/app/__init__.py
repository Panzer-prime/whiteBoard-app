from flask import Flask
from flask_socketio import SocketIO, send, emit
from app.socket import socket
from app.updateWhiteBoard import UpdateCardsPostion_bg
from app.handleRoomJoing import joinRoom_bg

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    socket.init_app(app, cors_allowed_origins="*")

    app.register_blueprint(joinRoom_bg)
    app.register_blueprint(UpdateCardsPostion_bg)

    #app.register_blueprint
    return app
