class Sensor:
    """
    A class which represents single sensor.

    Attributes
    ----------
    id: number
        identity of given sensor - must be unique
    x: number
        x position on sensing environment map (related to env width)
    y: number
        y position on sensing environment map (related to env length)
    sensing_range: number
        current range in which sensor is covering area - we assume that higher sensing_range higher battery consumption
        is
    max_sensing_range: number
        this value limits sensing_range
    operational_range: number
        range in which sensor can check whether other sensors are covering area around him, cannot be lower than
        max_sensing_range
    sens_frequency: number
        it says how often sensing occurs in some abstract time unit (e.g. seconds)
    sens_offset: number
        it says how much time after sensor started first sensing occurs (e.g. 10 seconds after start)
    """

    def __init__(self, id, x, y, sensing_range=0, max_sensing_range=5, operational_range=6, sens_frequency=30,
                 sens_offset=0):
        assert operational_range >= max_sensing_range
        self.id = id
        self.x = x
        self.y = y
        self.max_sensing_range = max_sensing_range
        if sensing_range > max_sensing_range:
            self.sensing_range = max_sensing_range
        else:
            self.sensing_range = sensing_range
        self.sens_frequency = sens_frequency
        self.sens_offset = sens_offset
        self.operational_range = operational_range

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
        elif new_sensing_range > self.max_sensing_range:
            self.sensing_range = self.max_sensing_range

    def details(self, advanced=False):
        details = self.__str__() + f' - s_range:{self.sensing_range}, o_range:{self.operational_range}, ' \
                                   f'ms_range:{self.max_sensing_range}'
        if advanced:
            return details + f' - off:{self.sens_offset},freq:{self.sens_frequency}'
        else:
            return details
