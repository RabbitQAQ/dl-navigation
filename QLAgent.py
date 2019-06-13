import random
import sys

import numpy as np
import pandas as pd

from MapEnv import Point


class QLAgent:
    def __init__(self, epsilon, learning_rate, discount_factor, actions):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.actions = actions
        self.Q_table = pd.DataFrame(columns=actions)

    def learn(self, cur_state, action, reward, next_state):
        self.create_state(next_state)
        q_predict = self.Q_table.loc[cur_state, action]
        if self.not_finished(reward):
            q_reality = reward + self.discount_factor * self.Q_table.loc[next_state, :].max()
        else:
            q_reality = reward
        self.Q_table.loc[cur_state, action] += self.learning_rate * (q_reality - q_predict)

    def create_state(self, state):
        if state not in self.Q_table.index:
            self.Q_table = self.Q_table.append(
                pd.Series(
                    data=[0] * len(self.actions),
                    index=self.actions,
                    name=state
                )
            )

    def init_index(self, max_row, max_col):
        index = []
        for row in range(max_row):
            for col in range(max_col):
                index.append(Point(row, col).toString())
        return index

    def choose_action(self, state):
        self.create_state(state)
        temp = np.random.uniform()

        if temp < self.epsilon:
            actions = self.Q_table.loc[state, :]
            action = self.choose_best_action(actions)
        elif temp >= self.epsilon:
            action = np.random.choice(self.actions)

        return action

    def not_finished(self, reward):
        return reward < 800 and reward > -800

    def choose_best_action(self, actions):
        q_table_cols = self.Q_table.columns
        max_action_value = -sys.maxsize
        max_action_value_list = []

        for i in range(len(q_table_cols)):
            action_value = actions[i]
            q_tabl_col = q_table_cols[i]

            if action_value > max_action_value:
                max_action_value = action_value
                max_action_value_list = [q_tabl_col]
            elif action_value == max_action_value:
                max_action_value_list.append(q_tabl_col)
            else:
                continue

        if len(max_action_value_list) > 1:
            random_action_index = random.randint(0, len(max_action_value_list) - 1)
            best_action = max_action_value_list[random_action_index]
        else:
            best_action = max_action_value_list[0]

        return best_action
