from datetime import datetime


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id}, ' +\
            f'timestamp={self.timestamp!r}, thought="{self.thought}")'

    def __str__(self):
        return f'[{self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}] ' +\
            f'user {self.user_id}: {self.thought}'

    def __eq__(self, value):
        return type(value) == Thought and self.user_id == value.user_id and \
            self.timestamp == value.timestamp and self.thought == value.thought

    def serialize(self):
        user_id_bytes = self.user_id.to_bytes(8, 'little')
        timestamp_bytes = int(self.timestamp.timestamp()).to_bytes(8, 'little')
        thought_bytes = self.thought.encode('utf8')
        thought_length_bytes = len(thought_bytes).to_bytes(4, 'little')
        return user_id_bytes + timestamp_bytes + \
            thought_length_bytes + thought_bytes

    def deserialize(data):
        user_id = int.from_bytes(data[0:8], 'little')
        timestamp = \
            datetime.fromtimestamp(int.from_bytes(data[8:16], 'little'))
        thought = data[20:].decode('utf8')
        return Thought(user_id, timestamp, thought)
