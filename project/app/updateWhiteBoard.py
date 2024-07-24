from app.socket import socket
from flask import Blueprint, request
from flask_socketio import emit

UpdateCardsPostion_bg = Blueprint("UpdateCardsPostion", __name__)


@socket.on("updateCardPosition")
def handleUpdatingCardsPostion(data):
    print(data)   
    emit("handleCardPosition", data, broadcast = True, )

@socket.on("handleOnNodeCreate")
def handleOnNodeCreate(data):
    if not data: return
    print("handleOnNodeCreate", data)
    emit("handleOnNodeCreate", data, broadcast=True)

@socket.on("handleOnDeleteNode")
def handleONdelete(id):
    if not id: return 
    print("id if the node: ", id)
    emit("handleOnDeleteNode", id, broadcast = True)


@socket.on("handlePropsChange")
def handlePropsChange(data):
    print("changed props of the node is: ",data)
    emit("handlePropsChange", data)