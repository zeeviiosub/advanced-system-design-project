from gzip import GzipFile
from utils.cortex_pb2 import User, Snapshot



#class Image:
#    def __init__(self, stream, image_type):
#        self.image_type = image_type
#        self.height, self.width = \
#            struct.unpack('II', stream.read(4 * 2))
#        self._pixel = []
#        for i in range(self.height):
#            self._pixel.append([])
#            for j in range(self.width):
#                if image_type == 'color':
#                    self._pixel[i].append(
#                        struct.unpack('BBB', stream.read(3)))
#                elif image_type == 'depth':
#                    self._pixel[i].append(
#                        struct.unpack('f', stream.read(4))[0])
#                else:
#                    raise Exception ('wrong image type')

#    def __getitem__(self, key):
#        return self._pixel[key]

#    def __repr__(self):
#        return f'<Image: {self.image_type} {self.height}x{self.width}>'

#class Snapshot:
#    def __init__(self, stream):
#        timestamp_bytes = stream.read(8)
#        if timestamp_bytes:
#            self.no_data = False
#        else:
#            self.no_data = True
#            return
#        timestamp = int.from_bytes(timestamp_bytes, 'little') / 1000
#        self.datetime = datetime.fromtimestamp(timestamp)
#        self.translation = struct.unpack('ddd', stream.read(8 * 3))
#        self.rotation = struct.unpack('dddd', stream.read(8 * 4))
#        self.color_image = Image(stream, 'color')
#        self.depth_image = Image(stream, 'depth')
#        self.hunger, self.thirst, self.exhaustion, self.happiness = \
#            struct.unpack('ffff', stream.read(4 * 4))

#class Reader:
#    def __init__(self, file_name):
#        self.stream = open(file_name, 'rb')
#        self.user_id = int.from_bytes(self.stream.read(8), 'little')
#        str_len = int.from_bytes(self.stream.read(4), 'little')
#        self.username = self.stream.read(str_len).decode()
#        timestamp = int.from_bytes(self.stream.read(4), 'little')
#        self.birth_date = date.fromtimestamp(timestamp)
#        self.gender = self.stream.read(1).decode()

#    def __iter__(self):
#        snapshot = Snapshot(self.stream)
#        while not snapshot.no_data:
#            yield snapshot
#            snapshot = Snapshot(self.stream)
#        self.stream.close()
class Reader:
    def __init__(self, file_name):
        self._stream = GzipFile(file_name, 'rb')
        user_len = int.from_bytes(self._stream.read(4), 'little')
        self.user = User()
        self.user.ParseFromString(self._stream.read(user_len))

    def __iter__(self):
        snapshot_len_bytes = self._stream.read(4)
        while snapshot_len := int.from_bytes(snapshot_len_bytes, 'little'):
            snapshot = Snapshot()
            snapshot.ParseFromString(self._stream.read(snapshot_len))
            yield snapshot
            snapshot_len_bytes = self._stream.read(4)
        self._stream.close()
