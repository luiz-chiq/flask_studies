from flask import Flask, jsonify, redirect, url_for, request
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB("todo_db.json")
Todo = Query()  

users = db.table('users')

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()  # Obter os dados do JSON na requisição
    if 'login' in data and 'name' in data:
        login = data['login']
        name = data['name']

        if (users.get(Todo.login == login) != None):
                return jsonify({'message': 'Usuário já existe'}), 409
        
        user = {'login': login, 'name': name}
        users.insert(user)
        
        return jsonify({'message': 'Usuário criado com sucesso!'}), 201
    else:
        return jsonify({'message': 'Dados incompletos'}), 400

if __name__ == '__main__':
    app.run()