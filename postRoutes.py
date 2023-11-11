from app import app, db
from tinydb import Query
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.post import Post
from models.UserLikePost import UserLikePost
from utils.modules import *

users = db.table('users')
posts = db.table('posts')
userLikePost = db.table('user_like_post')

@app.route('/createPost', methods=['POST'])
@jwt_required()
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
@jwt_required()
def remove_post():
    data = request.get_json()
    if 'id' not in data:
         return jsonify({'message': 'Dados incompletos'}), 400
    
    removedPost = posts.remove(Query().uuid == data['id'])
    if (len(removedPost) == 0):
        return jsonify({'message': 'Post não encontrado'}), 404
    return jsonify({'message': 'Post excluido com sucesso!'}), 200

@app.route('/updatePost', methods=['PUT'])
@jwt_required()
def update_post():
    
    data = request.get_json()
    dataToBeUpdated = {}

    if 'id' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    if not posts.contains(Query().uuid == data['id']):
        return jsonify({'message': 'Post não encontrado'}), 404
    
    if 'content' in data:
        dataToBeUpdated['content'] = data['content']
        
    posts.update(dataToBeUpdated, Query().uuid == data['id'])
    return jsonify({'message': 'Post atualizado com sucesso!'}), 200

@app.route('/likePost/<postId>', methods=['PUT'])
@jwt_required()
def like_post(postId):
    post = posts.get(Query().uuid == postId)
    if post == None:
        return jsonify({'message': 'Post não encontrado'}), 404
    
    userLogin = get_jwt_identity().get('login')

    if (userLikePost.contains(Query().user_login == userLogin)):
         return jsonify({'message': 'Usuário já curtiu o post informado'}), 400
    
    currentLikes = post.get('likes')

    posts.update({'likes': currentLikes + 1}, Query().uuid == postId)

    userLogin = get_jwt_identity().get('login')

    userLikedPost = UserLikePost(userLogin, postId)
    userLikePost.insert(userLikedPost.__dict__)
    
    return jsonify({'message': 'Post curtido com sucesso!'}), 200

@app.route('/unlikePost/<postId>', methods=['PUT'])
@jwt_required()
def unlike_post(postId):
    post = posts.get(Query().uuid == postId)
    if post == None:
        return jsonify({'message': 'Post não encontrado'}), 404
    
    userLogin = get_jwt_identity().get('login')

    if (not userLikePost.contains(Query().user_login == userLogin)):
         return jsonify({'message': 'Usuário não curtiu o post informado'}), 400
    
    currentLikes = post.get('likes')

    posts.update({'likes': currentLikes - 1}, Query().uuid == postId)

    userLogin = get_jwt_identity().get('login')

    userLikePost.remove(Query().user_login == userLogin and Query().post_id == postId)
    
    return jsonify({'message': 'Post descurtido com sucesso!'}), 200

@app.route('/getPosts', methods=['GET'])
def get_posts():
    postsPerPage = 10

    offset = len(posts)-postsPerPage
    offset -= int(request.args.get('offset', 0))
    if offset < 0:
        offset = 0
    pagedPosts = list(reversed(posts.all()[offset : offset + postsPerPage]))

    return jsonify(pagedPosts), 200