from app import app, db
from tinydb import Query
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

users = db.table('users')

@app.route('/getUsers', methods=['GET'])
def get_users():
   data = users.all()
   logins_list = [{"login": item["login"]} for item in data]
   return logins_list

@app.route('/getUserInfo', methods=['GET'])
@jwt_required()
def get_user_info():
    currentUser = users.get(Query().login == get_jwt_identity()["login"])
    currentUser.pop("password")
    return currentUser

@app.route('/createUser', methods=['POST'])
def create_user():

    data = request.get_json()

    if 'login' not in data or 'name' not in data or 'password' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    user = User(data['name'], data['login'], data["password"])
    if users.contains(Query().login == user.login):
        return jsonify({'message': 'Usuário já existe'}), 409

    users.insert(user.__dict__)
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

@app.route('/updateUser', methods=['PUT'])
@jwt_required()
def update_user():
    
    data = request.get_json()
    currentUser = get_jwt_identity()["login"]
    dataToBeUpdated = {}

    if 'name' in data:
        dataToBeUpdated['name'] = data['name']

    if 'password' in data:
         dataToBeUpdated['password'] = data['password']

    if dataToBeUpdated == {}:
        return jsonify({'message': 'Dados incompletos'}), 400
       
    users.update(dataToBeUpdated, Query().login == currentUser)
    return jsonify({'message': 'Usuário editado com sucesso!'}), 201

@app.route('/removeUser', methods=['DELETE'])
@jwt_required()
def remove_user():
    users.remove(Query().login == get_jwt_identity()["login"])
    return jsonify({'message': 'Usuário removido com sucesso'}), 201
