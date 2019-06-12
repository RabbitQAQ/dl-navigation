import os

from MapActions import MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN
from MapEnv import MapEnv, Point
from QLAgent import QLAgent
import tkinter as tk
from tkinter import *
from enum import Enum


class Operation(Enum):
    OBSTACLE = 1
    DANGER_1 = 2
    DANGER_2 = 3
    DANGER_3 = 4
    DANGER_4 = 5
    ERASER = 6
    START = 7
    END = 8


if __name__ == '__main__':
    # Global Variables
    MAX_ROW = 10
    MAX_COL = 10
    # Traveler/ destination/ obstacles setup
    traveler = Point(-1, -1)
    destination = Point(-1, -1)
    obstacles = []
    crime_low = []
    crime_mid = []
    crime_high = []
    crime_extreme = []
    startLearning = False
    # =================== GUI Mark Tool ====================
    # Create a grid of None to store the references to the tiles
    tiles = [[None for _ in range(MAX_COL)] for _ in range(MAX_ROW)]
    marker = [[None for _ in range(MAX_COL)] for _ in range(MAX_ROW)]
    currentMode = Operation.OBSTACLE
    # Create the window, a canvas and the mouse click event binding
    root = tk.Tk()
    img = PhotoImage(file="evanston_crime_small.png")
    c = tk.Canvas(root, width=img.width(), height=img.height(), borderwidth=5, background='white')
    c.create_image(0, 0, anchor=NW, image=img)
    c.pack()
    col_width = -1
    row_height = -1
    def mark(event):
        global traveler
        global destination
        global col_width
        global row_height
        col_width = c.winfo_width() / MAX_COL
        row_height = c.winfo_height() / MAX_ROW
        # Calculate column and row number
        col = int(event.x // col_width)
        row = int(event.y // row_height)
        # If the tile is not filled, create a rectangle
        if not tiles[row][col] and currentMode == Operation.OBSTACLE:
            c.create_rectangle(col * col_width, row * row_height, (col + 1) * col_width,
                               (row + 1) * row_height, fill="black")
            tiles[row][col] = -1000
            obstacles.append(Point(row, col))
        if not tiles[row][col] and currentMode == Operation.DANGER_1:
            marker[row][col] = c.create_rectangle(col * col_width, row * row_height, (col + 1) * col_width,
                               (row + 1) * row_height, fill="blue")
            tiles[row][col] = -30
            crime_low.append(Point(row, col))
        if not tiles[row][col] and currentMode == Operation.DANGER_2:
            marker[row][col] = c.create_rectangle(col * col_width, row * row_height, (col + 1) * col_width,
                               (row + 1) * row_height, fill="yellow")
            tiles[row][col] = -100
            crime_mid.append(Point(row, col))
        if not tiles[row][col] and currentMode == Operation.DANGER_3:
            marker[row][col] = c.create_rectangle(col * col_width, row * row_height, (col + 1) * col_width,
                               (row + 1) * row_height, fill="orange")
            tiles[row][col] = -400
            crime_high.append(Point(row, col))
        if not tiles[row][col] and currentMode == Operation.DANGER_4:
            marker[row][col] = c.create_rectangle(col * col_width, row * row_height, (col + 1) * col_width,
                               (row + 1) * row_height, fill="red")
            tiles[row][col] = -800
            crime_extreme.append(Point(row, col))
        if not tiles[row][col] and currentMode == Operation.START:
            if traveler.row == -1 and traveler.col == -1:
                traveler = Point(row, col)
                marker[row][col] = c.create_rectangle(col * col_width, row * row_height, (col + 1) * col_width,
                                   (row + 1) * row_height, fill="green")
                tiles[row][col] = 1

        if not tiles[row][col] and currentMode == Operation.END:
            if destination.row == -1 and destination.col == -1:
                destination = Point(row, col)
                marker[row][col] = c.create_rectangle(col * col_width, row * row_height, (col + 1) * col_width,
                                   (row + 1) * row_height, fill="green")
                tiles[row][col] = 1000
        if tiles[row][col] and currentMode == Operation.ERASER:
            if traveler.row == row and traveler.col == col:
                traveler = Point(-1, -1)
            if destination.row == row and destination.col == col:
                destination = Point(-1, -1)
            c.delete(marker[row][col])
            marker[row][col] = None
            tiles[row][col] = None
            obstacles.remove(Point(row, col))
            crime_low.remove(Point(row, col))
            crime_mid.remove(Point(row, col))
            crime_high.remove(Point(row, col))
            crime_extreme.remove(Point(row, col))
        c.update()


    c.bind("<Button-1>", mark)
    c.bind("<B1-Motion>", mark)


    def obstacleBtnHandler(event):
        global currentMode
        currentMode = Operation.OBSTACLE


    def danger1BtnHandler(event):
        global currentMode
        currentMode = Operation.DANGER_1


    def danger2BtnHandler(event):
        global currentMode
        currentMode = Operation.DANGER_2


    def danger3BtnHandler(event):
        global currentMode
        currentMode = Operation.DANGER_3


    def danger4BtnHandler(event):
        global currentMode
        currentMode = Operation.DANGER_4


    def eraserBtnHandler(event):
        global currentMode
        currentMode = Operation.ERASER


    def startBtnHandler(event):
        global currentMode
        currentMode = Operation.START


    def endBtnHandler(event):
        global currentMode
        currentMode = Operation.END

    def startLearningBtnHandler(event):
        print("wow")
        refresh_interval = 0.01
        # Number of iterations
        episode = 200
        # QLearning settings
        epsilon = 0.9
        learning_rate = 0.05
        discount_factor = 0.9
        # Move choices
        actions = [MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN]
        # Init map environment using the variables above
        env = MapEnv(
            max_row=MAX_ROW,
            max_col=MAX_COL,
            traveler=traveler,
            destination=destination,
            obstacles=obstacles,
            refresh_interval=refresh_interval,
            crime_low=crime_low,
            crime_mid=crime_mid,
            crime_high=crime_high,
            crime_extreme=crime_extreme,
        )
        # Init learning agent
        agent = QLAgent(
            epsilon=epsilon,
            learning_rate=learning_rate,
            discount_factor=discount_factor,
            actions=actions
        )
        successful_routines = []
        failed_routines = []
        # Show the map
        env.display()

        for eps in range(1, episode + 1):
            # Start from init location
            cur_state = env.reset()
            step_counter = 0

            while True:
                step_counter += 1

                env.display()

                c.delete(marker[env.traveler.row][env.traveler.col])
                marker[env.traveler.row][env.traveler.col] = None
                action = agent.choose_action(cur_state)

                next_state, reward = env.move(action)
                marker[env.traveler.row][env.traveler.col] = c.create_rectangle(env.traveler.col * col_width, env.traveler.row * row_height,
                                                                                (env.traveler.col + 1) * col_width,
                                                                                (env.traveler.row + 1) * row_height, fill="green")
                c.update()

                agent.learn(
                    cur_state=cur_state,
                    action=action,
                    reward=reward,
                    next_state=next_state
                )

                cur_state = next_state

                if reward > 800 or reward < -800:
                    # if reward != 0:
                    break

            if reward > 800:
                successful_routines.append(step_counter)
            elif reward < -800:
                failed_routines.append(step_counter)

            print(
                'total episode: {}\n'
                'current episode: {}\n'
                'reward: {}\nsteps: {}\n'
                'successful steps record: {}\n'
                'failed steps record: {}'
                    .format(
                    episode,
                    eps,
                    reward,
                    step_counter,
                    successful_routines,
                    failed_routines
                )
            )


    obstacleBtn = Button(root, text="Obstacle")
    danger1Btn = Button(root, text="Danger Zone 1")
    danger2Btn = Button(root, text="Danger Zone 2")
    danger3Btn = Button(root, text="Danger Zone 3")
    danger4Btn = Button(root, text="Danger Zone 4")
    eraserBtn = Button(root, text="Eraser")
    startBtn = Button(root, text="Start")
    endBtn = Button(root, text="End")
    startLearningBtn = Button(root, text="Start Learning", width=20, height=10)
    obstacleBtn.pack()
    danger1Btn.pack()
    danger2Btn.pack()
    danger3Btn.pack()
    danger4Btn.pack()
    eraserBtn.pack()
    startBtn.pack()
    endBtn.pack()
    startLearningBtn.pack()
    obstacleBtn.bind("<Button-1>", obstacleBtnHandler)
    danger1Btn.bind("<Button-1>", danger1BtnHandler)
    danger2Btn.bind("<Button-1>", danger2BtnHandler)
    danger3Btn.bind("<Button-1>", danger3BtnHandler)
    danger4Btn.bind("<Button-1>", danger4BtnHandler)
    eraserBtn.bind("<Button-1>", eraserBtnHandler)
    startBtn.bind("<Button-1>", startBtnHandler)
    endBtn.bind("<Button-1>", endBtnHandler)
    startLearningBtn.bind("<Button-1>", startLearningBtnHandler)

    # =================== GUI Mark Tool ====================
    root.mainloop()
