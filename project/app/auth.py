# auth_system.py
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, get_jwt_identity
from app.connectOnDB import connect_on_db, close_db_connection
from dotenv import load_dotenv
import os

load_dotenv()

# Flask Blueprints and Extensions
authSystem = Blueprint("authSystem", __name__)
bcrypt = Bcrypt()
jwt = JWTManager()

@authSystem.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    user = get_user_by_email(email)
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"msg": "Invalid email or password"}), 403
    
    access_token, refresh_token = create_tokens(user["user_id"], email)
    return jsonify({"msg": "Login successful", "token": access_token, "refresh_token": refresh_token}), 200

@authSystem.route("/api/auth/sign-up", methods=["POST"])
def sign_up():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"msg": "Email and password must not be empty"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    if create_user(email, hashed_password):
        user = get_user_by_email(email)
        access_token, refresh_token = create_tokens(user["user_id"], email)
        return jsonify({"msg": "User created successfully", "token": access_token, "refresh_token": refresh_token}), 201
    else:
        return jsonify({"msg": "Failed to create user"}), 500

@authSystem.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": new_access_token}), 200

def create_tokens(user_id, email):
    access_token = create_access_token(identity={'user_id': user_id, 'email': email})
    refresh_token = create_refresh_token(identity={'user_id': user_id, 'email': email})
    return access_token, refresh_token

def get_user_by_email(email: str):
    """Retrieve a user's hashed password and ID by their email."""
    conn = connect_on_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT password, userID FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user:
            return {"password": user[0], "user_id": user[1]}
        return None
    except Exception as error:
        print(f"Error fetching user: {error}")
        return None
    finally:
        cur.close()
        close_db_connection(conn)

def create_user(email: str, hashed_password: str):
    """Create a new user in the database."""
    conn = connect_on_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
        conn.commit()
        return True
    except Exception as error:
        print(f"Error creating user: {error}")
        return False
    finally:
        cur.close()
        close_db_connection(conn)
