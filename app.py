from flask import Flask
from tinydb import TinyDB
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '0hl96@pk&h@2=ds$n=#szu+ddkf$21bzrrph40#7zna3c_i^g_'

jwt = JWTManager(app)

db = TinyDB("db.json")

from routes import userRoutes, postRoutes, postCommentRoutes, authRoutes

if __name__ == '__main__':
    app.run()