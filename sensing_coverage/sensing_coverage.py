import gym.spaces as spaces
from pettingzoo.utils import ParallelEnv

# actions are: sens (range diff, freq diff, offset diff) - tuple of 3 ints
# rewards for each agent are: (
# global: (all_coverage: float 0-1, freq_all, jitter),
# local: (agent_coverage: float 0-1, other_agents_his_area_coverage: float 0-1, agent_freq, agent_offset)
# )
from sensing_coverage.sensing_render import SensingEnvRender

encode_multiplier = 10


class SensingCoverageParallel(ParallelEnv):
    def __init__(self, env, max_sensing_range=5, max_freq=50, max_offset=50, alpha=0.4):
        self.env = env
        self.max_sensing_range = max_sensing_range
        self.max_freq = max_freq
        self.alpha = alpha
        self.max_offset = max_offset
        self.render_env = SensingEnvRender(env)

    def render(self, mode="accurate"):
        if mode == "accurate":
            self.render_env.render_accurate()
        else:
            self.render_env.render_human()

    def get_render_env(self):
        return self.render_env

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
        all_freq = self.__sum_frequencies()
        jitter = self.env.get_jitter()
        for sensor_id, sensor in self.env.get_sensors():
            operational_coverage = self.env.get_covered_area_for_sensor_operational_range(
                sensor) / self.env.get_operational_max_for_sensor(sensor)
            other_coverage = self.env.get_covered_by_other_sensors(sensor) / area
            observation = {
                'global': {'coverage': all_coverage, 'freq': all_freq, 'jitter': jitter},
                'local': {
                    'coverage': operational_coverage, 'other_coverage': other_coverage,
                    'freq': sensor.sens_frequency, 'offset': sensor.sens_offset,
                }
            }
            if sensor.crashed:
                rewards[sensor_id] = 0
            elif sensor.sensing_range == 0:
                rewards[sensor_id] = self.alpha * operational_coverage + (1 - self.alpha)
            else:
                rewards[sensor_id] = self.alpha * operational_coverage + (1 - self.alpha) / sensor.sensing_range
            dones[sensor_id] = False
            infos[sensor_id] = None
            observations[sensor_id] = observation

        return observations, rewards, dones, infos

    def observation_space(self, agent):
        return spaces.Dict({
            'global': spaces.Dict(
                {
                    'coverage': spaces.Box(low=0, high=1.0),
                    'freq': spaces.Discrete(self.max_freq * len(self.env.get_sensors)),
                    'jitter': spaces.Box(low=0, high=self.max_freq)
                }
            ),
            'local': spaces.Dict(
                {
                    'coverage': spaces.Box(low=0, high=1.0),
                    'other_coverage': spaces.Box(low=0, high=1.0),
                    'freq': spaces.Discrete(self.max_freq),
                    'offset': spaces.Discrete(self.max_offset),
                }
            )}
        )

    def encode_state(self, self_cov, sens_range):
        self_cov_part = self_cov * self.max_sensing_range
        return self_cov_part + sens_range

    def states_amount(self):
        return encode_multiplier * encode_multiplier * encode_multiplier * self.max_sensing_range

    def action_space(self, agent):
        return spaces.MultiDiscrete([self.max_sensing_range * 2, self.max_freq * 2, self.max_offset * 2])

    def __sum_frequencies(self):
        sum_freq = 0
        for sensor_id, sensor in self.env.get_sensors():
            sum_freq += sensor.sens_frequency
        return sum_freq
