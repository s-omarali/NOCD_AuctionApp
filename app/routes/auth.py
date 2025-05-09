from flask import Flask
from flask_jwt_extended import JWTManager,create_access_token
from flask import Blueprint, request, jsonify
from models.User import User
from bcrypt import hashpw, gensalt, checkpw # going to use for password hashing


auth_bp = Blueprint('auth',__name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    phone_number = data.get("phone_number")

    
    existing_user = User.get_by_username(username)
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    
    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    
    new_user = User(username=username, phone_number=phone_number, password=hashed_password.decode('utf-8')) # new user instance
    new_user.save()

    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201

@auth_bp.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.get_by_username(username)
    if not user or user.password!= password:
        return jsonify({"error":" Incorrect password or invalid username "}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200
