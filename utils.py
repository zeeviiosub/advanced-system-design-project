import os
import os.path

class Context:

    def __init__(self):
        self._path = os.getcwd()

    def path(self, file_name):
        return os.path.join(self._path, file_name)
