import hmac
import hashlib
import base64
import json 
import datetime
from flask import Flask, jsonify, redirect, url_for, request
from tinydb import TinyDB, Query
from models.user import User
from models.post import Post

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


@app.route('/createPost', methods=['POST'])
def create_post():
    data = request.get_json()
    if 'login' not in data or 'content' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    post = Post(data['login'], data['content'])
    if not users.contains(Query().login == post.user_login):
        return jsonify({'message': 'Usuário não existe'}), 409
    
    posts.insert(post.__dict__)
    return jsonify({'message': 'Post feito con sucesso'}), 201

@app.route('/getPosts', methods=['GET'])
def get_posts():
    r = ''
    for post in posts.all():
        print(post)
        r += f"<h2>{post['user_login']}</h2>"
        r += f"<p>{post['content']}</p>"
    return r


secret_key = '52d3f853c19f8b63c0918c126422aa2d99b1aef33ec63d41dea4fadf19406e54'

@app.route('/createJWT')
def create_jwt():
    payload = {
        'userId': 'lac',
        'exp': (datetime.datetime.now() + datetime.timedelta(minutes=1)).timestamp(),
    }
    payload = json.dumps(payload).encode()
    header = json.dumps({
        'typ': 'JWT',
        'alg': 'HS256'
    }).encode()
    b64_header = base64.urlsafe_b64encode(header).decode()
    b64_payload = base64.urlsafe_b64encode(payload).decode()
    signature = hmac.new(
        key=secret_key.encode(),
        msg=f'{b64_header}.{b64_payload}'.encode(),
        digestmod=hashlib.sha256
    ).digest()
    jwt = f'{b64_header}.{b64_payload}.{base64.urlsafe_b64encode(signature).decode()}'
    return jwt

@app.route('/verify')
def verify_and_decode_jwt(jwt):
    b64_header, b64_payload, b64_signature = jwt.split('.')
    b64_signature_checker = base64.urlsafe_b64encode(
        hmac.new(
            key=secret_key.encode(),
            msg=f'{b64_header}.{b64_payload}'.encode(),
            digestmod=hashlib.sha256
        ).digest()
    ).decode()


    # payload extraido antes para checar o campo 'exp'
    payload = json.loads(base64.urlsafe_b64decode(b64_payload))
    unix_time_now = datetime.datetime.now().timestamp()

    if payload.get('exp') and payload['exp'] < unix_time_now:
        raise Exception('Token expirado')
    
    if b64_signature_checker != b64_signature:
        raise Exception('Assinatura inválida')
    
    return payload    

if __name__ == '__main__':
    app.run()
    
    print("payload: ", payload)
    jwt_created = create_jwt(payload)
    print(jwt_created)
    decoded_jwt = verify_and_decode_jwt(jwt_created)
    print(decoded_jwt)
    # print(validate(jwt_created))