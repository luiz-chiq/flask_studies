from flask import Flask
from tinydb import TinyDB
import uuid
from flask_jwt_extended import JWTManager
from utils.modules import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '0hl96@pk&h@2=ds$n=#szu+ddkf$21bzrrph40#7zna3c_i^g_'

jwt = JWTManager(app)

db = TinyDB("db.json")

import userRoutes
import postRoutes
import authRoutes

@app.route('/uuid', methods=['GET'])
def generate_uuid():
    id = f'<h1>{uuid.uuid4()}</h1>'
    return id

if __name__ == '__main__':
    app.run()