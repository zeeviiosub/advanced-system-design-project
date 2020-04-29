import redis

class Saver:

    def __init__(self, db_url):
        self.r = redis.from_url(db_url)

    def save(self, field, data):
        snapshot, real_data = data.split(sep=b'*', maxsplit=1)
        self.r.set(field, real_data, snapshot)
