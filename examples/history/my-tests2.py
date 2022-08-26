from qlearning_agent import QLearningAgent
from sensing_coverage.sensing_coverage import SensingCoverageParallel
from sensing_coverage.sensing_environment import SensingEnvironment
from sensing_coverage.sensor import Sensor


def iql():
    how_many_iter_prints = 25
    iterations = 100000

    max_sens_range = 6
    cov_multiplier = 5
    env_alpha = 0.8

    sensor0 = Sensor(0, 3, 2, sensing_range=1, max_sensing_range=max_sens_range)
    sensor1 = Sensor(1, 9, 7, sensing_range=1, max_sensing_range=max_sens_range)
    sensor2 = Sensor(2, 4, 9, sensing_range=1, max_sensing_range=max_sens_range)
    sensor3 = Sensor(3, 7, 2, sensing_range=1, max_sensing_range=max_sens_range)

    sensors_dict = {0: sensor0, 1: sensor1, 2: sensor2, 3: sensor3}
    sensing_env = SensingEnvironment(sensors=sensors_dict, width=12, length=12)
    parallel_env = SensingCoverageParallel(env=sensing_env, max_sensing_range=max_sens_range, alpha=env_alpha)

    states_amount = cov_multiplier * max_sens_range + max_sens_range + 1
    actions_amount = max_sens_range * 2
    q_agent_learn_rate = 0.1
    q_agent_epsilon = 0.1
    q_agent_discount_rate = 0.7
    q_agents = [
        QLearningAgent(states_amount, actions_amount, q_agent_learn_rate, q_agent_epsilon, q_agent_discount_rate)
        for _ in range(len(sensors_dict))
    ]
    should_render = False
    states = {0: None, 1: None, 2: None, 3: None}
    rewards_to_check = []
    coverages_to_check = []
    ranges_to_check = []
    for it in range(iterations):
        actions = {}
        for ind, q_agent in enumerate(q_agents):
            action = q_agent.select_action(states[ind])
            actions[ind] = (action - max_sens_range, 0, 0)
        observations, rewards, dones, infos = parallel_env.step(actions)
        rewards_to_check.extend(rewards.values())
        coverages_to_check.extend(cov['local']['coverage'] for cov in observations.values())
        ranges_to_check.extend(sensor.sensing_range for sensor in sensors_dict.values())

        for ind, q_agent in enumerate(q_agents):
            reward = rewards[ind]
            old_state = states[ind]
            observation = observations[ind]
            self_cov_state = int(observation['local']['coverage'] * cov_multiplier)
            new_state = parallel_env.encode_state(self_cov_state, sensors_dict[ind].sensing_range)
            states[ind] = new_state
            q_agent.update(reward, new_state, actions[ind][0] + max_sens_range, old_state)
        iterations_per_batch = int(iterations / how_many_iter_prints)
        if it % iterations_per_batch == 0 and it > 0:
            if should_render:
                parallel_env.render()
            print(f'IT: {it}')
            print('mean rewards:' + str(sum(rewards_to_check) / len(rewards_to_check)))
            print('mean coverages:' + str(sum(coverages_to_check) / len(coverages_to_check)))
            print('mean ranges:' + str(sum(ranges_to_check) / len(ranges_to_check)))
            mean_cov_for_last_batch = sum(coverages_to_check[-iterations_per_batch:]) / iterations_per_batch
            mean_sens_range_for_last_batch = sum(ranges_to_check[-iterations_per_batch:]) / iterations_per_batch
            print(f'mean coverages for last {iterations_per_batch} iters: {mean_cov_for_last_batch}')
            print(f'mean sensing ranges for last {iterations_per_batch} iters: {mean_sens_range_for_last_batch}')
            print('---------------------------------------------------------------------------------------------------')
    parallel_env.render()
    print(f'At the end after {iterations} iterations')
    for sensor_id, sensor in sensors_dict.items():
        print(
            f'Sensor: {sensor.details()}, State: {states[sensor_id]}, Reward: {rewards[sensor_id]}, Coverage: {observations[sensor_id]["local"]["coverage"]}')
        print()
    print('mean rewards:' + str(sum(rewards_to_check) / len(rewards_to_check)))
    print('mean coverages:' + str(sum(coverages_to_check) / len(coverages_to_check)))
    print('mean ranges:' + str(sum(ranges_to_check) / len(ranges_to_check)))
    print('------------------------------------------------------------------------------------------------------')
