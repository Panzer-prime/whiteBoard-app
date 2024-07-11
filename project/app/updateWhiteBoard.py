from app.socket import socket
from flask import Blueprint, request
from flask_socketio import emit

UpdateCardsPostion_bg = Blueprint("UpdateCardsPostion", __name__)


@socket.on("updateCardPosition")
def handleUpdatingCardsPostion(data):
    print(data)   
    emit("handleCardPosition", data, broadcast = True, )


