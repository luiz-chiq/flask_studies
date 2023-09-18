import uuid

class User:
    def __init__(self, name, login):
        self.name = name
        self.login = login
        self.uuid = str(uuid.uuid4())
    