import uuid

class Comment:
    def __init__(self, post_id, user, content):
        self.user = user
        self.post_id = post_id
        self.content = content
        self.uuid = str(uuid.uuid4())