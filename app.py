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