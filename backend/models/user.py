import uuid

class User:
    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password
        self.uuid = str(uuid.uuid4())
    