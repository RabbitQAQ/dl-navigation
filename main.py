from MapEnv import MapEnv, Point
from QLAgent import QLAgent
from MapActions import MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN


if __name__ == '__main__':
    refresh_interval = 0.05

    episode = 150

    epsilon = 0.9
    learning_rate = 0.05
    discount_factor = 0.9  #

    max_row = 19
    max_col = 7
    actions = [MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN]
    worker = Point(3, 6)
    treasure = Point(0, 5)
    crime_low = [
        Point(0, 1),
        Point(0, 6),
        Point(2, 1),
        Point(2, 6),
        Point(3, 4),
        Point(4, 6),
        Point(6, 1),
        Point(6, 3),
        Point(6, 5),
        Point(8, 3),
        Point(8, 5),
        Point(9, 4),
        Point(9, 6),
        Point(10, 5),
        Point(11, 4),
        Point(13, 0),
        Point(13, 6),
        Point(14, 1),
        Point(14, 3),
        Point(15, 0),
        Point(16, 1),
        Point(16, 4),
        Point(17, 4),
        Point(18, 1),
    ]

    crime_mid = [
        Point(0, 3),
        Point(4, 5),
        Point(10, 3),
        Point(13, 2),
        Point(17, 6),
        Point(18, 2),
        Point(18, 5),

    ]

    crime_high = [
        Point(8, 1),
        Point(18, 0),

    ]

    crime_extreme = [
        Point(5, 6),


    ]



    obstacles = [
        Point(1, 1),
        Point(1, 3),
        Point(1, 5),
        Point(3, 1),
        Point(3, 3),
        Point(3, 5),
        Point(5, 1),
        Point(5, 3),
        Point(5, 5),
        Point(7, 1),
        Point(7, 3),
        Point(7, 5),
        Point(9, 1),
        Point(9, 3),
        Point(9, 5),
        Point(11, 1),
        Point(11, 3),
        Point(11, 5),
        Point(13, 1),
        Point(13, 3),
        Point(13, 5),
        Point(15, 1),
        Point(15, 3),
        Point(15, 5),
        Point(17, 1),
        Point(17, 3),
        Point(17, 5),


    ]

    env = MapEnv(
        max_row=max_row,
        max_col=max_col,
        traveler=worker,
        destination=treasure,
        obstacles=obstacles,
        crime_extreme=crime_extreme,
        crime_low=crime_low,
        crime_mid=crime_mid,
        crime_high=crime_high,
        refresh_interval=refresh_interval
    )
    agent = QLAgent(
        epsilon=epsilon,
        learning_rate=learning_rate,
        discount_factor=discount_factor,
        actions=actions
    )
    successful_step_counter_arr = []
    failed_step_counter_arr = []

    env.display()

    for eps in range(1, episode + 1):

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

            if reward > 800 or reward < -800:

            # if reward != 0:
                break

        if reward > 800:
            successful_step_counter_arr.append(step_counter)
        elif reward < -800:
            failed_step_counter_arr.append(step_counter)

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
                successful_step_counter_arr,
                failed_step_counter_arr
            )
        )


        # print(agent.q_table)
        # print('successful steps record: {}'.format(succeed_step_counter_arr))