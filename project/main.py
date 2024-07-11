from app import create_app
from app.socket import socket
from flask_socketio import emit

app = create_app()
@socket.on("message")
def onMessage(message):
    print("message", f"the message received is this one: {message}" )




if __name__ == "__main__":
    print("Starting Flask-SocketIO server...")
    socket.run(app, debug=True)
