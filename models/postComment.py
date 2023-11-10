import uuid

class PostComment:
    def __init__(self, post_id, user_id, content):
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.uuid = str(uuid.uuid4())