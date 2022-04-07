from gym.spaces import Discrete

from pettingzoo.utils import ParallelEnv
from sensing_environment import SensingEnvironment
from sensing_render import SensingEnvRender
from sensor import Sensor


# actions are: sens (range diff, freq diff, offset diff) - tuple of 3 ints
# rewards for each agent are: (
# global: (all_coverage: float 0-1, freq_all, jitter),
# local: (agent_coverage: float 0-1, other_agents_his_area_coverage: float 0-1, agent_freq, agent_offset)
# )

class parallel_env(ParallelEnv):
    def __init__(self, env, max_sensing_range=5):
        self.env = env
        self.max_sensing_range = max_sensing_range
        self.render_env = SensingEnvRender(env)

    def render(self, mode="human"):
        self.render_env.render()

    def step(self, actions):
        for sensor_id, actions in actions.items():
            if actions is not None:
                (range_diff, freq_diff, offset_diff) = actions
                sensor = self.env.get_sensor(sensor_id)
                sensor.adjust_sensing_range(range_diff)
                sensor.adjust__frequency(freq_diff)
                sensor.adjust__offset(offset_diff)

        rewards = {}
        observations = {}
        dones = {}
        infos = {}
        area = self.env.get_area()
        all_coverage = self.env.get_covered_area() / area
        all_freq = 0
        self.__sum_frequencies()
        jitter = 0  # TODO std od sredniej odleglosci miedzy pomiarami, rozlozyc na osi np. od kazdego sensora 1000, posortowac na osi i wyjac lacznie 1000 pomiarow
        for sensor_id, sensor in self.env.get_sensors():
            sensor_coverage = self.env.get_covered_area_for_sensor(sensor) / area
            other_coverage = self.env.get_covered_by_other_sensors(sensor) / area
            observation = {
                'global': {'coverage': all_coverage, 'freq': all_freq, 'jitter': jitter},
                'local': {
                    'coverage': sensor_coverage, 'other_coverage': other_coverage,
                    'freq': sensor.sens_frequency, 'offset': sensor.sens_offset,
                }
            }

            rewards[sensor_id] = all_coverage  #shouldn't we use more complex formula using e.g. sensing range?
            dones[sensor_id] = False
            infos[sensor_id] = None
            observations[sensor_id] = observation

        return observations, rewards, dones, infos

    def observation_space(self, agent):
        pass
        # TODO

    def action_space(self, agent):
        return Discrete(self.max_sensing_range * 2 + 1)

    def __sum_frequencies(self):
        sum_freq = 0
        for sensor_id, sensor in self.env.get_sensors():
            sum_freq += sensor.sens_frequency
        return sum_freq


def example_1():
    sensor0 = Sensor(0, 1, 1, 2)
    sensor1 = Sensor(1, 2, 5, 4)
    sensor2 = Sensor(2, 12, 9, 6)
    sensors = {0: sensor0, 1: sensor1, 2: sensor2}
    sensing_env = SensingEnvironment(sensors, 25, 25)
    # print(sensing_env.get_sensing_coverage())
    print(sensing_env.get_coverage_by_other_sensors_area(sensor0))
    par_env = parallel_env(sensing_env)
    par_env.render()
    # rend_env = SensingEnvRender(sensing_env)
    # rend_env.render_environment(25, 25, sensing_env.get_coverage_for_sensor_area(sensor2))


def example_2():
    sensor0 = Sensor(0, 1, 1, 2)
    sensor1 = Sensor(1, 2, 5, 4)
    sensor2 = Sensor(2, 12, 9, 6)
    sensors = {0: sensor0, 1: sensor1, 2: sensor2}
    sensing_env = SensingEnvironment(sensors, 25, 25)
    par_env = parallel_env(sensing_env)
    actions = {0: (2, 0, 3), 1: (3, 1, -54), 2: (4, 6, 3)}
    res = par_env.step(actions)
    print(res)


if __name__ == '__main__':
    example_1()
