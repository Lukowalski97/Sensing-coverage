import math

import numpy as np


class SensingEnvironment:
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
        '''
        :returns 2D array bool array where True means positions covered by sensor of given sensor_id
        '''
        sensing_range = sensor.sensing_range
        (xx, yy) = np.ogrid[:self.width, :self.length]
        dist_from_center = np.sqrt((xx - sensor.x) ** 2 + (yy - sensor.y) ** 2)
        covered_area = dist_from_center <= sensing_range
        return covered_area

    def get_sensing_coverage_area(self):
        '''
        :returns 2D array bool array where True means positions covered by some sensor
        '''
        return self.get_coverage_excluding_sensor_area()

    def get_coverage_excluding_sensor_area(self, sensor=None):
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

    def get_coverage_by_other_sensors_area(self, sensor):
        check_range = sensor.check_range  #
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
        sensors_measures = np.full(self.jitter_time_max, False)
        for sensor_id, sensor in self.get_sensors():
            tmp_measure = sensor.sens_offset
            while tmp_measure < self.jitter_time_max:
                sensors_measures[tmp_measure] = True
                tmp_measure += sensor.sens_frequency

        last_ind_measured = -1
        gaps_amount = 0
        measures_gap_sum = 0
        measures_gaps = []
        for ind, measured in enumerate(sensors_measures):
            if measured:
                if last_ind_measured > -1:
                    gaps_amount += 1
                    gap = ind - last_ind_measured
                    measures_gap_sum += gap
                    measures_gaps.append(gap)
                last_ind_measured = ind

        average_gap = measures_gap_sum / gaps_amount
        variance = 0
        for gap in measures_gaps:
            variance += ((gap - average_gap) ** 2)
        return math.sqrt(variance)

    def get_covered_by_other_sensors(self, sensor):
        return self.__get_covered_for_array(self.get_coverage_by_other_sensors_area(sensor))

    def get_covered_area(self):
        coverage = self.get_sensing_coverage_area()
        return self.__get_covered_for_array(coverage)

    def get_covered_area_for_sensor(self, sensor):
        return self.__get_covered_for_array(self.get_coverage_for_sensor_area(sensor))

    def __get_covered_for_array(self, arr):
        covered_fields = 0
        for x in arr:
            for y in x:
                if y:
                    covered_fields += 1
        return covered_fields
