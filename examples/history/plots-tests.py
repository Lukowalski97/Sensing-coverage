import matplotlib.pyplot as plt

from examples.qlearning_agent import QLearningAgent
from sensing_coverage.sensing_coverage import SensingCoverageParallel
from sensing_coverage.sensing_environment import SensingEnvironment
from sensing_coverage.sensor import Sensor

# This version has const q_agent_epsilon, nothing special in scenario
def iql():
    env_alphas = [0, 0.2, 0.4, 0.6, 0.8, 1]

    for env_alpha in env_alphas:
        plot_window_size = 250
        iterations = 3000

        max_sens_range = 6
        cov_multiplier = 5

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
        q_agent_epsilon = 0.05
        q_agent_discount_rate = 0.7
        q_agents = [
            QLearningAgent(states_amount, actions_amount, q_agent_learn_rate, q_agent_epsilon, q_agent_discount_rate)
            for _ in range(len(sensors_dict))
        ]
        states = {0: None, 1: None, 2: None, 3: None}
        local_coverages = {0: [], 1: [], 2: [], 3: []}
        local_ranges = {0: [], 1: [], 2: [], 3: []}
        local_rewards = {0: [], 1: [], 2: [], 3: []}

        global_coverages = []
        mean_ranges = []
        mean_rewards = []

        x_axis = []

        local_coverages_axis = {0: [], 1: [], 2: [], 3: []}
        local_ranges_axis = {0: [], 1: [], 2: [], 3: []}
        local_rewards_axis = {0: [], 1: [], 2: [], 3: []}

        global_coverages_axis = []
        mean_ranges_axis = []
        mean_rewards_axis = []
        for it in range(iterations):
            actions = {}
            for ind, q_agent in enumerate(q_agents):
                action = q_agent.select_action(states[ind])
                actions[ind] = (action - max_sens_range, 0, 0)
            observations, rewards, dones, infos = parallel_env.step(actions)



            for ind, q_agent in enumerate(q_agents):
                local_coverages[ind].append(observations[ind]['local']['coverage'])
                local_ranges[ind].append(sensors_dict[ind].sensing_range)
                local_rewards[ind].append(rewards[ind])

            global_coverages.append(observations[0]['global']['coverage'])
            mean_ranges.append(sum(sensor.sensing_range for sensor in sensors_dict.values())/ len(sensors_dict))
            mean_rewards.append(sum(reward for reward in rewards.values())/ len(sensors_dict))

            if it % plot_window_size == 0:
                for ind, q_agent in enumerate(q_agents):
                    local_coverages_axis[ind].append(sum(local_coverages[ind][-plot_window_size:]) / plot_window_size)
                    local_ranges_axis[ind].append(sum(local_ranges[ind][-plot_window_size:]) / plot_window_size)
                    local_rewards_axis[ind].append(sum(local_rewards[ind][-plot_window_size:]) /plot_window_size)

                global_coverages_axis.append(sum(global_coverages[-plot_window_size:])/plot_window_size)
                mean_ranges_axis.append(sum(mean_ranges[-plot_window_size:])/plot_window_size)
                mean_rewards_axis.append(sum(mean_rewards[-plot_window_size:])/plot_window_size)
                x_axis.append(it)

            for ind, q_agent in enumerate(q_agents):
                reward = rewards[ind]
                old_state = states[ind]
                observation = observations[ind]
                self_cov_state = int(observation['local']['coverage'] * cov_multiplier)
                new_state = parallel_env.encode_state(self_cov_state, sensors_dict[ind].sensing_range)
                states[ind] = new_state
                q_agent.update(reward, new_state, actions[ind][0] + max_sens_range, old_state)

        print('PLOTS')
        fig, axs = plt.subplots(2,3, figsize=(13,10))
        fig.suptitle(f'Env alpha: {env_alpha}')
        ax_local_cov = axs[0, 0]
        ax_local_ran = axs[0, 1]
        ax_local_rew = axs[0, 2]
        ax_global_cov = axs[1, 0]
        ax_global_ran = axs[1, 1]
        ax_global_rew = axs[1, 2]
        for ind, q_agent in enumerate(q_agents):
            ax_local_cov.plot(x_axis, local_coverages_axis[ind], label=f's{ind}')
            ax_local_ran.plot(x_axis, local_ranges_axis[ind], label=f's{ind}')
            ax_local_rew.plot(x_axis, local_rewards_axis[ind], label=f's{ind}')

        ax_global_cov.plot(x_axis, global_coverages_axis)
        ax_global_ran.plot(x_axis, mean_ranges_axis)
        ax_global_rew.plot(x_axis, mean_rewards_axis)

        ax_local_cov.set_title('Local Coverage')
        ax_local_cov.set_ylim([0, 1])
        ax_local_cov.legend(loc='upper right', bbox_to_anchor=(-0.2, 0))
        ax_local_ran.set_title('Local Ranges')
        ax_local_ran.set_ylim([0, 6])
        ax_local_rew.set_title('Local Rewards')
        ax_local_rew.set_ylim([0, 1])

        ax_global_cov.set_title('Global Coverage')
        ax_global_cov.set_ylim([0, 1])
        ax_global_ran.set_title('Mean ranges')
        ax_global_ran.set_ylim([0, 6])
        ax_global_rew.set_title('Mean rewards')
        ax_global_rew.set_ylim([0, 1])

        fig.tight_layout()
        plt.savefig(f'out/iqlv1-{int(env_alpha * 10)}')


if __name__ == '__main__':
    iql()
