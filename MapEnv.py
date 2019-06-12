import os
import time

import numpy as np

from MapActions import MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN


class MapEnv:
    def __init__(self, max_row, max_col, traveler, destination, crime_high, crime_low, crime_mid, crime_extreme, refresh_interval, obstacles=None, ):
        self.max_row = max_row
        self.max_col = max_col
        self.init_worker = traveler.clone()
        self.traveler = traveler
        self.destination = destination
        self.crime_high = crime_high
        self.crime_mid = crime_mid
        self.crime_low = crime_low
        self.crime_extreme = crime_extreme
        self.refresh_interval = refresh_interval

        if obstacles:
            for obstacle in obstacles:
                if destination.equal(obstacle):
                    raise Exception('The treasure point is conflicted with an obstacle point')
            self.obstacles = obstacles
        else:
            self.obstacles = []

    def move(self, action):
        if action == MOVE_LEFT:
            if self.traveler.col > 0:
                self.traveler.col -= 1
        elif action == MOVE_RIGHT:
            if self.traveler.col < self.max_col - 1:
                self.traveler.col += 1
        elif action == MOVE_UP:
            if self.traveler.row > 0:
                self.traveler.row -= 1
        elif action == MOVE_DOWN:
            if self.traveler.row < self.max_row - 1:
                self.traveler.row += 1
        else:
            raise Exception('Not supported action: {}'.format(action))

        return self.feedback()

    def feedback(self):
        state = self.traveler.toString()
        reward = 0
        if self.traveler.equal(self.destination):
            reward = 1000
        for low in self.crime_low:
            if self.traveler.equal(low):
                reward -= 30
        for mid in self.crime_mid:
            if self.traveler.equal(mid):
                reward -= 100
        for high in self.crime_high:
            if self.traveler.equal(high):
                reward -= 400
        for extreme in self.crime_extreme:
            if self.traveler.equal(extreme):
                reward -= 800
        for obstacle in self.obstacles:
            if self.traveler.equal(obstacle):
                reward = -1000
        return state, reward

    def reset(self):
        self.traveler = self.init_worker.clone()
        return self.traveler.toString()

    def display(self):
        os.system('clear')
        arr = np.zeros((self.max_row, self.max_col))
        arr[self.destination.row][self.destination.col] = 8
        arr[self.traveler.row][self.traveler.col] = 1
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
        #time.sleep(self.refresh_interval)


class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def equal(self, other_point):
        return self.row == other_point.row and self.col == other_point.col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def toString(self):
        return "({},{})".format(str(self.row), str(self.col))

    def clone(self):
        return Point(self.row, self.col)
