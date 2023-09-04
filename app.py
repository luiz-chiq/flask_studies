from flask import Flask, jsonify, redirect, url_for, request
from tinydb import TinyDB, Query
from models.user import User

app = Flask(__name__)
db = TinyDB("db.json")
Todo = Query()  

users = db.table('users')
posts = db.table('posts')
likes = db.table('likes')

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()  # Obter os dados do JSON na requisição
    if 'login' not in data or 'name' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    user = User(data['name'], data['login'])
    if users.contains(Query().login == user.login):
        return jsonify({'message': 'Usuário já existe'}), 409
    
    users.insert(user.__dict__)
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

if __name__ == '__main__':
    app.run()