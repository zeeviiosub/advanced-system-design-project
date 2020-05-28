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
            print(f'THE FIELD IS {field}')
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


serializers = {}
deserializers = {}
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

    def serializer(field):
        def wrapper(function):
            serializers[field] = function
            return function
        return wrapper

    @serializer('pose')
    def serialize_pose(self):
        return struct.pack('fffffff', *self.translation, *self.rotation)

    @serializer('color_image')
    def serialize_color_image(self):
        return ('color_image_' + str(self.timestamp) + '.png').encode('utf8')

    @serializer('depth_image')
    def serialize_depth_image(self):
        return ('depth_image_' + str(self.timestamp) + '.png').encode('utf8')

    @serializer('feelings')
    def serialize_feelings(self):
        feelings = self.hunger, self.thirst, self.exhaustion, self.happiness
        return struct.pack('ffff', *feelings)

    @serializer('timestamp')
    def serialize_timestamp(self):
        return self.timestamp.to_bytes(8, 'little')

    def serialize_field(self, field):
        return serializers[field](self)

    def deserializer(field):
        def wrapper(function):
            deserializers[field] = function
            return function
        return wrapper

    @deserializer('pose')
    def deserialize_pose(pose_bytes):
        translation = struct.unpack('ffff', pose_bytes[0:16])
        rotation = struct.unpack('fff', pose_bytes[16:28])
        return translation, rotation
    
    @deserializer('color_image')
    def deserialize_color_image(color_image_bytes):
        return color_image_bytes.decode('utf8')

    @deserializer('depth_image')
    def deserialize_depth_image(depth_image_bytes):
        return depth_image_bytes.decode('utf8')

    @deserializer('feelings')
    def deserialize_feelings(feelings_bytes):
        return struct.unpack('ffff', feelings_bytes)

    @deserializer('timestamp')
    def deserialize_timestamp(timestamp_bytes):
        return int.from_bytes(timestamp_bytes, 'little')
    
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
            print(f'colour image size: {width*height*3}')
            data = data + self.color_image.data
            #for i in range(width*height*3):
                #data = data + struct.pack('B', self.color_image.data[i])
                #if i % 10000 == 0:
                    #print(i)
        
        width = self.depth_image.width
        data = data + width.to_bytes(4, 'little')
        if not width:
            data = data + b'\x00\x00\x00\x00'
        else:
            height = self.depth_image.height
            data = data + height.to_bytes(4, 'little')
            print(f'depth image size: {width*height}')
            data = data + self.depth_image.data
            #for i in range(width*height):
                #data = data + struct.pack('B', self.depth_image.data[i])
                #if i % 10000 == 0:
                    #print(i)
        
        data = data + struct.pack('ffff', self.hunger, self.thirst,
            self.exhaustion, self.happiness)
        return data

    def deserialize(data):
        print(f'data={data}')
        print(f'len(data)={len(data)}')
        snapshot = Snapshot(int.from_bytes(data[0:8], 'little'))
        snapshot.translation = struct.unpack('ddd', data[8:32])
        snapshot.rotation = struct.unpack('dddd', data[32:64])
        snapshot.color_image.width = int.from_bytes(data[64:68], 'little')
        print(snapshot.color_image.width)
        snapshot.color_image.height = int.from_bytes(data[68:72], 'little')
        #next_byte = 64
        print(data[72:72+snapshot.color_image.width*snapshot.color_image.height*3])

        snapshot.color_image.data = \
            data[72:72+snapshot.color_image.width*snapshot.color_image.height*3]
        next_byte = \
            72 + snapshot.color_image.width*snapshot.color_image.height*3
        #for i in range(width):
        #    snapshot.color_image.append([])
        #    for j in range(height):
        #        snapshot.color_image[i].append(\
        #            struct.unpack('BBB', data[next_byte:next_byte+3]))
        #        next_byte = next_byte + 3
        snapshot.depth_image.width = int.from_bytes(data[next_byte:next_byte+4], 'little')
        snapshot.depth_image.height = int.from_bytes(data[next_byte+4:next_byte+8], 'little')
        for i in range(snapshot.depth_image.width*snapshot.depth_image.height):
            snapshot.depth_image.data.append(
                struct.unpack('f', data[next_byte+8+i*4:next_byte+8+i*4+4]
            ))
        #snapshot.depth_image.data = data[next_byte+8:next_byte+8+width*height]
        next_byte = \
            next_byte + 8 + \
            snapshot.depth_image.width*snapshot.depth_image.height*4
        #next_byte = next_byte + 8
        #for i in range(width):
        #    snapshot.depth_image.append([])
        #    for j in range(height):
        #        snapshot.depth_image[i].append(\
        #            struct.unpack('BBB', data[next_byte:next_byte+3]))
        #        next_byte = next_byte + 3
        snapshot.hunger, snapshot.thirst, snapshot.exhaustion, snapshot.happiness = \
            struct.unpack('ffff', data[next_byte:next_byte+16])
        return snapshot
