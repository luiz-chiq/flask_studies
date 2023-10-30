from app import app, db
from tinydb import Query
from flask import jsonify, request
from flask_jwt_extended import create_access_token

users = db.table('users')

@app.route("/login", methods=["POST"])
def login():
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    if (login == None or password == None):
        return jsonify({'message': 'Dados incompletos'}), 400
    user = users.get(Query().login == login and Query().password == password)
    if user == None:
        return jsonify({"message": "Login ou senha incorretos"}), 401

    access_token = create_access_token(identity={"login": login, "id": user.get("uuid")})
    return jsonify(access_token=access_token)