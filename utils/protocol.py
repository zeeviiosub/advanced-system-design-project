import datetime
import struct
from cortex_pb2 import ColorImage, DepthImage

class Hello:
    def __init__(self, user_id, username, birth_date, gender):
        self.user_id = user_id
        self.username = username
        self.birth_date = birth_date
        self.gender = gender

    def serialize(self):
        user_id_bytes = self.user_id.to_bytes(8, 'little')
        username_bytes = self.username.encode('utf8')
        username_len_bytes = len(username_bytes).to_bytes(4, 'little')
        birth_date_bytes = (int(self.birth_date)).to_bytes(4, 'little')
        gender_byte = self.gender.encode('utf8')
        return user_id_bytes + birth_date_bytes + gender_byte + \
            username_len_bytes + username_bytes

    def deserialize(data):
        user_id = int.from_bytes(data[0:8], 'little')
        birth_date = int.from_bytes(data[8:12], 'little')
        gender = data[12:13].decode('utf8')
        username_len = int.from_bytes(data[13:17], 'little')
        username = data[17:17+username_len].decode('utf8')
        return Hello(user_id, username, birth_date, gender)

    def __repr__(self):
        return f'Hello({self.user_id:r}, {self.username:r}, ' + \
            f'{self.birth_date:r}, {self.gender:r})'

    def __eq__(self, other):
        return self.user_id == other.user_id and \
            self.username == other.username and \
            self.birth_date == other.birth_date  and \
            self.gender == other.gender

class Config:
    def __init__(self, *fields):
        self.fields = fields

    def serialize(self):
        data = len(self.fields).to_bytes(4, 'little')
        for field in self.fields:
            field_bytes = field.encode('utf8')
            data = data + len(field_bytes).to_bytes(4, 'little')
            data = data + field_bytes
        return data

    def deserialize(data):
        config = Config()
        num_of_fields = int.from_bytes(data[0:4], 'little')
        fields = []
        next_byte = 4
        for i in range(num_of_fields):
            str_len = int.from_bytes(data[next_byte:next_byte+4], 'little')
            next_byte = next_byte + 4
            fields.append(data[next_byte:next_byte+str_len].decode('utf8'))
            next_byte = next_byte + str_len
        return Config(*fields)


class Snapshot:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.translation = (0.0, 0.0, 0.0)
        self.rotation = (0.0, 0.0, 0.0, 0.0)
        self.color_image = ColorImage()
        self.depth_image = DepthImage()
        self.hunger = 0.0
        self.thirst = 0.0
        self.exhaustion = 0.0
        self.happiness = 0.0

    def serialize(self):
        data = self.timestamp.to_bytes(8, 'little')
        for datum in self.translation:
            data = data + struct.pack('d', datum)
        for datum in self.rotation:
            data = data + struct.pack('d', datum)
        width = self.color_image.width
        data = data + width.to_bytes(4, 'little')
        if not width:
            data = data + b'\x00\x00\x00\x00'
        else:
            height = self.color_image.height
            data = data + height.to_bytes(4, 'little')
            data = data + self.color_image.data
        
        width = self.depth_image.width
        data = data + width.to_bytes(4, 'little')
        if not width:
            data = data + b'\x00\x00\x00\x00'
        else:
            height = self.depth_image.height
            data = data + height.to_bytes(4, 'little')
            data_list = list(self.depth_image.data)
            data = data + struct.pack('f' * len(data_list), *data_list)
            #for datum in self.depth_image.data:
            #    data = data + struct.pack('f', datum)
        
        data = data + struct.pack('ffff', self.hunger, self.thirst,
            self.exhaustion, self.happiness)
        return data

    def deserialize(data):
        snapshot = Snapshot(int.from_bytes(data[0:8], 'little'))
        snapshot.translation = struct.unpack('ddd', data[8:32])
        snapshot.rotation = struct.unpack('dddd', data[32:64])
        snapshot.color_image.width = int.from_bytes(data[64:68], 'little')
        snapshot.color_image.height = int.from_bytes(data[68:72], 'little')

        snapshot.color_image.data = \
            data[72:72+snapshot.color_image.width*snapshot.color_image.height*3]
        next_byte = \
            72 + snapshot.color_image.width*snapshot.color_image.height*3
        snapshot.depth_image.width = int.from_bytes(data[next_byte:next_byte+4], 'little')
        snapshot.depth_image.height = int.from_bytes(data[next_byte+4:next_byte+8], 'little')
        for i in range(snapshot.depth_image.width*snapshot.depth_image.height):
            snapshot.depth_image.data.append(
                struct.unpack('f', data[next_byte+8+i*4:next_byte+8+i*4+4])[0]
            )
        next_byte = \
            next_byte + 8 + \
            snapshot.depth_image.width*snapshot.depth_image.height*4
        snapshot.hunger, snapshot.thirst, snapshot.exhaustion, snapshot.happiness = \
            struct.unpack('ffff', data[next_byte:next_byte+16])
        return snapshot
