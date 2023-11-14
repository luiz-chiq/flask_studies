from app import app, db
from tinydb import Query
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.comment import Comment

comments = db.table('postComments')
posts = db.table('posts')

@app.route('/getComments/<post_id>', methods=['GET'])
@jwt_required()
def get_comments(post_id):

    post_comments = comments.get(Query().post_id == post_id)

    if not post_comments:
        return jsonify({'message': 'Post não encontrado'}), 404
    
    return comments.get(Query().post_id == post_id)


@app.route('/createComment', methods=['POST'])
@jwt_required()
def create_comment():

    data = request.get_json()

    if 'content' not in data or 'post_id' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    if (not posts.contains(Query().uuid == data['post_id'])):
        return jsonify({'message': 'Postagem não encontrada'}), 404
    
    loggedUser = get_jwt_identity()["login"]
    
    comment = Comment(data['post_id'], loggedUser, data['content'])
    
    comments.insert(comment.__dict__)
    return jsonify({'message': 'Comentário criado com sucesso!'}), 201

@app.route('/updateComment', methods=['PUT'])
@jwt_required()
def update_comment():
    
    data = request.get_json()

    if 'comment_id' not in data or 'content' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    finded = find_comment(data)
    if finded != None:
        return finded

    dataToBeUpdated = {}
    dataToBeUpdated['content'] = data['content']

    comments.update(dataToBeUpdated, Query().uuid == data['comment_id'])
       
    return jsonify({'message': 'Comentário editado com sucesso!'}), 201

@app.route('/removeComment', methods=['DELETE'])
@jwt_required()
def remove_comment():

    data = request.get_json()

    if 'comment_id' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    finded = find_comment(data)
    if finded != None:
        return finded

    comments.remove(Query().uuid == data['comment_id'])
   
    return jsonify({'message': 'Comentário removido com sucesso'}), 201

def find_comment(data):
    
    comment = comments.get(Query().uuid == data['comment_id'])

    if (comment == None):
        return jsonify({'message': 'Comentário não encontrado'}), 404
    
    if (comment["user"] != get_jwt_identity()["login"]):
        return jsonify({'message': 'Apenas o dono desse comentário pode editá-lo'}), 401