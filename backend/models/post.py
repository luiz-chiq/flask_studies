import uuid

class Post:
    def __init__(self, user_login, content):
        self.user_login = user_login
        self.content = content
        self.likes = 0
        self.uuid = str(uuid.uuid4())