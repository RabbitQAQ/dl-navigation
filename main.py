from MapActions import MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN
from MapEnv import MapEnv, Point
from QLAgent import QLAgent

if __name__ == '__main__':
    refresh_interval = 0.05
    # Number of iterations
    episode = 100
    # QLearning settings
    epsilon = 0.9
    learning_rate = 0.05
    discount_factor = 0.9
    # Map settings
    max_row = 5
    max_col = 5
    # Move choices
    actions = [MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN]
    # Traveler/ destination/ obstacles setup
    traveler = Point(0, 0)
    destination = Point(2, 2)
    obstacles = [
        Point(1, 2),
        Point(2, 1),
        Point(3, 1),
        Point(1, 3),
        Point(2, 3),
        Point(3, 3),
    ]
    # Init map environment using the variables above
    env = MapEnv(
        max_row=max_row,
        max_col=max_col,
        traveler=traveler,
        destination=destination,
        obstacles=obstacles,
        refresh_interval=refresh_interval
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

            action = agent.choose_action(cur_state)

            next_state, reward = env.move(action)

            agent.learn(
                cur_state=cur_state,
                action=action,
                reward=reward,
                next_state=next_state
            )

            cur_state = next_state

            if reward != 0:
                break

        if reward > 0:
            successful_routines.append(step_counter)
        elif reward < 0:
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
