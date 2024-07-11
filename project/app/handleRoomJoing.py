from app.socket import socket
from flask import Blueprint
from flask_socketio import join_room, send, leave_room



joinRoom_bg = Blueprint("handleRoomJoing", __name__)

@socket.on("join")
def joinRoom(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    send("username")

#we leave a room based on some kind of id     
@socket.on("leave")
def leaveRoom(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send
    