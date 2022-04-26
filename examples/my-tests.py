from sensing_coverage.sensor import Sensor
from sensing_coverage.sensing_coverage import encode_multiplier
from sensing_coverage.sensing_environment import SensingEnvironment
from sensing_coverage.sensing_coverage import SensingCoverageParallel


def init():
    sensor0 = Sensor(id=0, x=4, y=5, sensing_range=12)
    sensor1 = Sensor(id=1, x=0, y=0, sensing_range=1, max_sensing_range=7, check_range=4, sens_frequency=30,
                     sens_offset=15)

    my_sensors = {0: sensor0, 1: sensor1}
    sensing_env = SensingEnvironment(sensors=my_sensors, width=25, length=30)

    sensing_coverage_env = SensingCoverageParallel(env=sensing_env, max_sensing_range=7, max_freq=40, max_offset=40)
    observations, rewards, dones, infos = sensing_coverage_env.step({})
    print(observations)
    print(rewards)
    # sensing_coverage_env.render()
    return sensing_coverage_env


def test_encoding(sensing_coverage_env):
    max_iter = encode_multiplier * encode_multiplier * encode_multiplier * 7
    errors = []
    for i in range(max_iter):
        self_cov, other_cov, glob_cov, sens_range = sensing_coverage_env.decode_state(i)
        encoded = sensing_coverage_env.encode_state(self_cov, other_cov, glob_cov, sens_range)
        print(
            f'state: {i}, self_cov: {self_cov}, other_cov: {other_cov}, glob_cov: {glob_cov}, sens_range: {sens_range}, encoded: {encoded}')
        if encoded != i:
            errors.append(i)

    assert len(errors) == 0


if __name__ == '__main__':
    init_env = init()
    test_encoding(init_env)
