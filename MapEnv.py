import os
import time

import numpy as np

from MapActions import MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN


class MazeEnv:
    def __init__(self, max_row, max_col, worker, treasure, crime_high, crime_low, crime_mid, crime_extreme, refresh_interval, obstacles=None,):
        self.max_row = max_row
        self.max_col = max_col
        self.init_worker = worker.clone()
        self.worker = worker
        self.treasure = treasure
        self.crime_high = crime_high
        self.crime_mid = crime_mid
        self.crime_low = crime_low
        self.crime_extreme = crime_extreme
        self.refresh_interval = refresh_interval

        if obstacles:
            for obstacle in obstacles:
                if treasure.equal(obstacle):
                    raise Exception('The treasure point is conflicted with an obstacle point')
            self.obstacles = obstacles
        else:
            self.obstacles = []

    def move(self, action):
        # print(action)

        if action == MOVE_LEFT:
            if self.worker.col > 0:
                self.worker.col -= 1
        elif action == MOVE_RIGHT:
            if self.worker.col < self.max_col - 1:
                self.worker.col += 1
        elif action == MOVE_UP:
            if self.worker.row > 0:
                self.worker.row -= 1
        elif action == MOVE_DOWN:
            if self.worker.row < self.max_row - 1:
                self.worker.row += 1
        else:
            raise Exception('Not supported action: {}'.format(action))

        return self.feedback()

    def feedback(self):
        state = self.worker.toString()
        reward = 0
        if self.worker.equal(self.treasure):
            reward = 1000
        for low in self.crime_low:
            if self.worker.equal(low):
                reward -= 30
        for mid in self.crime_mid:
            if self.worker.equal(mid):
                reward -= 100
        for high in self.crime_high:
            if self.worker.equal(high):
                reward -= 400
        for extreme in self.crime_extreme:
            if self.worker.equal(extreme):
                reward -= 800
        for obstacle in self.obstacles:
            if self.worker.equal(obstacle):
                reward = -1000
        return state, reward

    def reset(self):
        self.worker = self.init_worker.clone()
        return self.worker.toString()

    def display(self):
        os.system('clear')
        arr = np.zeros((self.max_row, self.max_col))
        arr[self.treasure.row][self.treasure.col] = 8
        arr[self.worker.row][self.worker.col] = 1
        for obstacle in self.obstacles:
            arr[obstacle.row][obstacle.col] = 7
        for low in self.crime_low:
            arr[low.row][low.col] = -1
        for mid in self.crime_mid:
            arr[mid.row][mid.col] = -2
        for high in self.crime_high:
            arr[high.row][high.col] = -3
        for extreme in self.crime_extreme:
            arr[extreme.row][extreme.col] = -4
        print(arr)
        time.sleep(self.refresh_interval)


class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def equal(self, other_point):
        return self.row == other_point.row and self.col == other_point.col

    def toString(self):
        return "({},{})".format(str(self.row), str(self.col))

    def clone(self):
        return Point(self.row, self.col)
