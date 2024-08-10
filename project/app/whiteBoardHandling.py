from app.socket import socket
from flask import Blueprint, request, jsonify, session as flask_session
from flask_socketio import emit, join_room, send
from uuid import uuid4  # You might want to use this for room or session IDs
from app.connectOnDB import connect_on_db, close_db_connection
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint setup
WhiteBoardHandle = Blueprint("WhiteBoardHandle", __name__)
bcrypt = Bcrypt()

# SocketIO event handlers
@socket.on("updateCardPosition")
def handleUpdatingCardsPosition(data):
    room = flask_session.get("room")
    if not room:
        emit("error", {"msg": "RoomID is needed"})
        return
    print(data)
    emit("handleCardPosition", data, broadcast=True, to=room)

@socket.on("handleOnNodeCreate")
def handleOnNodeCreate(data):
    room = flask_session.get("room")
    if not room:
        emit("error", {"msg": "RoomID is needed"})
        return
    
    newNode = data.get('newNode')
    emit("handleOnNodeCreate", newNode, to=room)

@socket.on("handleOnDeleteNode")
def handleOnDeleteNode(data):
    room = flask_session.get("room")
    if not room:
        emit("error", {"msg": "RoomID is needed"})
        return
    
    node_id = data.get("id")
    print(data)
    emit("handleOnDeleteNode", node_id, broadcast=True, to=room)

@socket.on("join")
def join(room_id: str):
    # Here, you are passing room_id as an argument but not using it
    # Updated to use the passed room_id directly
    flask_session["room"] = room_id
    print(room_id, "User joining room")
    join_room(room_id)
    send(f"New user connected to {room_id}", to=room_id)

# API routes
@WhiteBoardHandle.route("/api/getRoom", methods=['POST'])
@jwt_required()
def get_room_id():
    data = request.get_json()
    roomName = data.get("roomName")
    roomPass = data.get("roomPass")
    
    if not roomName or not roomPass:
        return jsonify({"msg": "roomPass and roomName are required"}), 400
    
    print(data, "Retrieved room ID")
    
    room_session = get_room_session(roomPass, roomName)
    
    if not room_session or not bcrypt.check_password_hash(room_session["roomPass"], roomPass):
        return jsonify({"msg": "Invalid room name or password"}), 403
    
    flask_session["room"] = roomName
    join_room(roomName)
    return jsonify({"msg": "Room session active"}), 200
  

@WhiteBoardHandle.route("/api/room/new", methods=['POST'])
@jwt_required()
def createNewRoomSession():
    data = request.get_json()
    roomName = data.get("roomName")
    roomPass = data.get("roomPass")
    user_email = get_jwt_identity().get("email")
    
    if not roomName or not roomPass:
        return jsonify({"msg": "roomPass and roomName are required"}), 400
    
    hashed_password = bcrypt.generate_password_hash(roomPass).decode("utf-8")
    if create_room_session(roomName, hashed_password, user_email):
        flask_session["room"] = roomName
        return jsonify({"msg": "Successfully created room session"}), 201
    else:
        return jsonify({"msg": "Failed to create room"}), 500

# Helper functions
def get_room_session(roomPass: str, roomName: str):
    conn = connect_on_db()
    try:
        with conn.cursor() as curr:
            curr.execute("SELECT sessionPassword FROM session WHERE sessionName = %s", (roomName,))
            room_session = curr.fetchone()
            if room_session: 
                return {"roomName": roomName, "roomPass": room_session[0]}
            
    except Exception as error:
        print("Failed to retrieve session:", error)
        return None
    finally:
        close_db_connection(conn)

def create_room_session(roomName, roomPass, user_email):
    conn = connect_on_db()
    try:
        with conn.cursor() as curr:
            curr.execute("INSERT INTO session (sessionName, sessionPassword, userEmail) VALUES (%s, %s, %s)", 
                         (roomName, roomPass, user_email))
            conn.commit()
            return True
    except Exception as error:
        print(f"Error creating room session: {error}")
        return False
    finally:
        close_db_connection(conn)
