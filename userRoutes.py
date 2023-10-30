from app import app, db
from tinydb import Query
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from models.user import User
from utils.modules import *

users = db.table('users')

@app.route('/getUsers', methods=['GET'])
def get_users():
    r = ''
    for user in users.all():
        r += f"<h2>ID: {user['uuid']}</h2>"
        r += f"<p>Login: {user['login']}</p>"
        r += f"<p>Nome: {user['name']}</p>"
    return r

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
    dataToBeUpdated = {}

    if 'login' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    isUserLogged = verifyIfIsLoggedUserByLogin(data['login'])
    if (not isUserLogged):
        return jsonify({'message': 'Apenas o dono desse usuário pode editá-lo'}), 401

    if 'name' in data:
        dataToBeUpdated['name'] = data['name']

    if 'password' in data:
         dataToBeUpdated['password'] = data['password']
       
    users.update(dataToBeUpdated, Query().login == data['login'])
    return jsonify({'message': 'Usuário editado com sucesso!'}), 201

@app.route('/removeUser', methods=['DELETE'])
@jwt_required()
def remove_user():
    data = request.get_json()
    if 'id' not in data:
         return jsonify({'message': 'Dados incompletos'}), 400
    
    removedUser = users.remove(Query().id == data['id'])
    if (len(removedUser) == 0):
        return jsonify({'message': 'Usuário não encontrado'}), 404
    return jsonify({'message': 'Usuário removido com sucesso'}), 201
