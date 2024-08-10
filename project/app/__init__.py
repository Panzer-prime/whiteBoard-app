import os 
from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.socket import socket
from app.auth import authSystem
from app.whiteBoardHandling import WhiteBoardHandle

from dotenv import load_dotenv

from datetime import timedelta

load_dotenv()


def create_app():

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv("JTW_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    print(os.getenv("JTW_SECRET_KEY"), "here you can see the env") 

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    socket.init_app(app, cors_allowed_origins="*")

    app.register_blueprint(WhiteBoardHandle)
    app.register_blueprint(authSystem)
    #app.register_blueprint
    return app
