from helper import read_data


class VectorData:
    def __init__(self, path):
        self.path = path
        self.data = read_data(self.path)
