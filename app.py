from flask import Flask, jsonify, redirect, url_for, request
from tinydb import TinyDB, Query
from models.user import User
from models.post import Post
import uuid

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

    data = request.get_json()

    if 'login' not in data or 'name' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    user = User(data['name'], data['login'])
    if users.contains(Query().login == user.login):
        return jsonify({'message': 'Usuário já existe'}), 409

    users.insert(user.__dict__)
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

@app.route('/updateUser', methods=['PUT'])
def update_user():
    
    data = request.get_json()
    dataToBeUpdated = {}

    if 'login' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    if 'name' in data:
        setattr(dataToBeUpdated, 'name', data['name'])
       
    users.update(dataToBeUpdated, Query().login == data['login'])

@app.route('/removeUser', methods=['DELETE'])
def remove_user():
    data = request.get_json()
    if 'id' not in data:
         return jsonify({'message': 'Dados incompletos'}), 400
    
    users.remove(Query().uuid == data['id'])


@app.route('/createPost', methods=['POST'])
def create_post():
    data = request.get_json()
    if 'user' not in data or 'content' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    post = Post(data['user'], data['content'])
    if not users.contains(Query().login == post.user_login):
        return jsonify({'message': 'Usuário não existe'}), 409
    
    posts.insert(post.__dict__)
    return jsonify({'message': 'Post feito com sucesso'}), 201

@app.route('/removePost', methods=['DELETE'])
def remove_post():
    data = request.get_json()
    if 'id' not in data:
         return jsonify({'message': 'Dados incompletos'}), 400
    
    posts.remove(Query().uuid == data['id'])
    return jsonify({'message': 'Post excluido com sucesso!'}), 200

@app.route('/updatePost', methods=['PUT'])
def update_post():
    
    data = request.get_json()
    dataToBeUpdated = {}

    if 'id' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    if 'content' in data:
        setattr(dataToBeUpdated, 'content', data['content'])
       
    posts.update(dataToBeUpdated, Query().uuid == data['id'])
    return jsonify({'message': 'Post atualizado com sucesso!'}), 200

@app.route('/getUsers', methods=['GET'])
def get_users():
    r = ''
    for user in users.all():
        r += f"<h2>{user['uuid']}</h2>"
        r += f"<p>{user['login']}</p>"
        r += f"<p>{post['name']}</p>"
    return r

@app.route('/getPosts', methods=['GET'])
def get_posts():
    r = ''
    for post in posts.all():
        print(post)
        r += f"<h2>{post['user_login']}</h2>"
        r += f"<p>{post['content']}</p>"
        r += f"<p>{post['uuid']}</p>"
    return r

@app.route('/uuid', methods=['GET'])
def generate_uuid():
    id = f'<h1>{uuid.uuid4()}</h1>'
    return id

if __name__ == '__main__':
    app.run()