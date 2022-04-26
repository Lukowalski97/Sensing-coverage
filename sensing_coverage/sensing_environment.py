import math

import numpy as np


class SensingEnvironment:
    """
    A class which represents sensing environment containing some sensors placed on rectangle map.


    Attributes
    ----------
    sensors: dict
        dicitonary where key is id of sensor and value is Sensor itself
    width(optional): number
        width of a sensing map rectangle
    length(optional): number
        length of a sensing map rectangle
    jitter_time_max: number
        when calculating jitter it is used to define how many units of time (e.g. seconds) are taken under
        consideration when creating a list of sensing measurements of each sensor
    """

    def __init__(self, sensors, width=5, length=5, jitter_time_max=10000):
        self.width = width
        self.length = length
        self.sensors = sensors
        self.jitter_time_max = jitter_time_max

    def get_area(self):
        return self.width * self.length

    def get_width(self):
        return self.width

    def get_length(self):
        return self.length

    def get_sensors(self):
        return self.sensors.items()

    def get_sensor(self, id):
        return self.sensors[id]

    def remove_sensor(self, sensor):
        self.sensors.pop(sensor.id)

    def get_coverage_for_sensor_area(self, sensor):
        """
        :returns 2D bool array where True means positions covered by sensor of given sensor_id
        """
        sensing_range = sensor.sensing_range
        (xx, yy) = np.ogrid[:self.width, :self.length]
        dist_from_center = np.sqrt((xx - sensor.x) ** 2 + (yy - sensor.y) ** 2)
        covered_area = dist_from_center <= sensing_range
        return covered_area

    def get_sensing_coverage_area(self):
        """
        :returns 2D bool array where True means positions covered by some sensor
        """
        return self.get_coverage_excluding_sensor_area()

    def get_coverage_excluding_sensor_area(self, sensor=None):
        """
        :return: 2D bool array where True means all map position covered by all sensors excluding sensor which is
        served as parameter
        """
        sensor_id = None
        if sensor is not None:
            sensor_id = sensor.id

        covered_area = np.full((self.width, self.length), False)
        for sensor in self.sensors.values():
            if sensor.id != sensor_id:
                area = self.get_coverage_for_sensor_area(sensor)
                for ind_y, row in enumerate(area):
                    for ind_x, x in enumerate(row):
                        if x and area[ind_y, ind_x]:
                            covered_area[(ind_x, ind_y)] = True
        return covered_area

    def __check_coverage_by_other_sensors_area(self, sensor):
        """
        :return: 2d bool array where True means position covered by other sensors limited to check_range of given sensor
        """
        check_range = sensor.check_range
        (xx, yy) = np.ogrid[:self.width, :self.length]
        dist_from_center = np.sqrt((xx - sensor.x) ** 2 + (yy - sensor.y) ** 2)
        covered_area = dist_from_center <= check_range

        result = np.full((self.width, self.length), False)
        for ind_y, row in enumerate(self.get_coverage_excluding_sensor_area(sensor)):
            for ind_x, x in enumerate(row):
                if x and covered_area[ind_y, ind_x]:
                    result[ind_x, ind_y] = True
        return result

    def get_jitter(self):
        """
        :return: calculates a jitter using standard deviation. First we create a bool array of False values called
        measures. Then we iterate over each sensor and calculate timestamps using sensor's sens_offset and
        sens_frequency - we fill measures array with True in places where timestamp occur.
        In next step we iterate over measures array to check gaps between each measure.
        Next we calculate avreage_gap by dividing sum of gaps and their amount. At last we iterate over each gap
        and to calculate standard deviation where average is average_gap and x_i is measured gap.
        """
        # todo -
        sensors_measures_occurences = set()  # we don't need duplicates
        for sensor_id, sensor in self.get_sensors():
            tmp_measure = sensor.sens_offset
            while tmp_measure < self.jitter_time_max:
                sensors_measures_occurences.add(tmp_measure)
                tmp_measure += sensor.sens_frequency
        sensors_measures_occurences = list(sensors_measures_occurences)
        sensors_measures_occurences.sort()

        prev_measure_occurrence = sensors_measures_occurences[0]
        gaps_amount = 0
        measures_gap_sum = 0
        measures_gaps = []
        for measure_occurrence in sensors_measures_occurences[1:]:
            gaps_amount += 1
            gap = measure_occurrence - prev_measure_occurrence
            measures_gap_sum += gap
            measures_gaps.append(gap)
            prev_measure_occurrence = measure_occurrence

        average_gap = measures_gap_sum / gaps_amount
        variance = 0
        for gap in measures_gaps:
            variance += ((gap - average_gap) ** 2)
        return math.sqrt(variance)

    def get_covered_by_other_sensors(self, sensor):
        """
        :return: a scalar number which indicates how many points on map are covered by other senors within given
        sensor's check range
        """
        return self.__get_covered_to_scalar(self.__check_coverage_by_other_sensors_area(sensor))

    def get_covered_area(self):
        """
        :return: a scalar number which indicates how many points on map are covered by all sensors
        """
        coverage = self.get_sensing_coverage_area()
        return self.__get_covered_to_scalar(coverage)

    def get_covered_area_for_sensor(self, sensor):
        """
        :return: a scalar number which indicates how many points on map are covered by given sensor
        """
        return self.__get_covered_to_scalar(self.get_coverage_for_sensor_area(sensor))

    def __get_covered_to_scalar(self, arr):
        covered_fields = 0
        for x in arr:
            for y in x:
                if y:
                    covered_fields += 1
        return covered_fields
