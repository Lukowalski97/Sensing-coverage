class Sensor:
    '''
    sens_frequency and sens_offset are in time unit which is one tick - it may be second/hours or sth like this
    x, y, sensing_range, max_sensing_range are in length units e.g. meters
    '''

    def __init__(self, id, x, y, sensing_range=0, max_sensing_range=5, check_range = 3, sens_frequency=30, sens_offset=0):
        self.id = id
        self.x = x
        self.y = y
        self.max_sensing_range = max_sensing_range
        self.sensing_range = sensing_range
        self.sens_frequency = sens_frequency
        self.sens_offset = sens_offset
        self.check_range = check_range

    def __str__(self):
        return f'{self.id}:({self.x},{self.y})'

    def set_coordinates(self, new_x=None, new_y=None):
        if new_x is not None:
            self.x = new_x
        if new_y is not None:
            self.y = new_y

    def adjust__frequency(self, diff):
        new_freq = self.sens_frequency + diff
        if 0 <= new_freq:
            self.sens_frequency = new_freq

    def adjust__offset(self, diff):
        new_offset = self.sens_offset + diff
        if 0 <= new_offset:
            self.sens_offset = new_offset

    def adjust_sensing_range(self, diff):
        new_sensing_range = self.sensing_range + diff
        if 0 <= new_sensing_range <= self.max_sensing_range:
            self.sensing_range = new_sensing_range
