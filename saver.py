import redis

class Saver:

    def __init__(self, db_url):
        self.r = redis.from_url(db_url)

    def save(self, field, data):
        self.r.set(field, data)
