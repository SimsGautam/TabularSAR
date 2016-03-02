from domain import *
from old_agent import *
import copy
import visualize
import threading
import time

def train(num_episodes, domain, agent):

    # print updates 10 times
    chunk_size = num_episodes/10
    print_mark = [chunk_size*i for i in range(10)]
    for episode in range(num_episodes):
        if episode in print_mark:
            print "Training " + str(episode) + "/" + str(num_episodes) + " complete."
        total_reward = 0
        domain.reinitialize()
        while True:
            state = domain.get_state()
            dup_state = copy.copy(state)
            action = agent.choose_action(state)
            is_terminal = domain.step(action)
            new_state = domain.get_state()
            if not is_terminal:
                # if the game has not ended, incur a cost of living reward
                reward = -0.1
                agent.Q_learn(dup_state, action, reward, new_state)
                total_reward += reward
            else:
                if domain.reached_goal():
                    # if the game ended and agent is at the goal
                    reward = 0
                else:
                    # if max_steps is reached and agent not at goal
                    reward = -0.1
                total_reward += reward
                new_state = domain.state
                agent.Q_learn(dup_state, action, reward, new_state)
                break


def test(num_episodes, domain, agent, display):

    for episode in range(num_episodes):
        total_reward = 0
        domain.reinitialize()
        while True:
            state = domain.get_state()
            dup_state = copy.copy(state)
            display.update_grid(dup_state)
            action = agent.choose_action(state)
            is_terminal = domain.step(action)
            if not is_terminal:
                # if the game has not ended, incur a cost of living reward
                reward = -0.1
                total_reward += reward
            else:
                if domain.reached_goal():
                    # if the game ended and agent is at the goal
                    reward = 0
                else:
                    # if max_steps is reached and agent not at goal
                    reward = -0.1
                total_reward += reward
                break
            time.sleep(0.5)
        print "Episode: " + str(episode) + ", Total Reward: " + str(total_reward)
        display.end_game()
    return True


if __name__ == '__main__':
    domain = MovingGoalsWorld()
    agent = OldAgent(domain.possible_actions)
    episodes_train = 15000
    episodes_test = 1

    train(episodes_train, domain, agent)

    # set the exploration rate to 0 before testing
    agent.set_epilson(0)

    while True:
        inp = raw_input('Enter test or quit: ')

        if inp == 'quit':
            break

        elif inp == 'test':
            display = visualize.VisualGame(domain.get_state())

            test_thread = threading.Thread(target = test, args = (episodes_test, domain, agent, display))
            display_thread = threading.Thread(target = display.run)

            test_thread.start()
            display_thread.start()

        else:
            continue
    