import numpy as np


class QLearningAgent:
    def __init__(self, states_n, actions_n, learning_rate, epsilon, discount_rate):
        self.__actions_n = actions_n
        self.__learning_rate = learning_rate
        self.__epsilon = epsilon
        self.__discount_rate = discount_rate
        self.__q_matrix = np.random.rand(states_n, actions_n)

    def select_action(self, state=None):
        if state is None:
            return self.select_random_action()
        random_num = np.random.rand()
        if random_num < self.__epsilon:
            return self.select_random_action()
        else:
            return np.argmax(self.__q_matrix[state])

    def select_random_action(self):
        return np.random.randint(0, self.__actions_n)

    def update(self, reward, new_state, action, old_state=None):
        if old_state is None:
            old_state = new_state
        current_value = self.__q_matrix[old_state][action]
        q_prim = self.__discount_rate * np.max(self.__q_matrix[new_state])
        self.__q_matrix[old_state][action] = current_value + self.__learning_rate * (reward - current_value + q_prim)

