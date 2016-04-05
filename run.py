from domain import *
from old_agent import *
from SASR_agent import *
import copy
import visualize
import multiprocessing
import time
import matplotlib
from operator import add
from operator import div
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def train(max_episodes, domain, agent, goal_index):
    chunk_size = 10
    rewards = []
    episode = 0
    while True:
        if episode % 10 == 0:
            print 'explored states: ' + str(agent.explored_SA_count)
            print "Training: " + str(episode) + " episodes complete."
            # print rewards[-chunk_size:]
            # if (len(set(rewards[-chunk_size:])) == 1 and rewards[-chunk_size:][0] > -3) or episode >= max_episodes:
            if episode > max_episodes:
                break
        total_reward = 0
        domain.reinitialize(goal_index)
        agent_alive = True
        while agent_alive:
            state = domain.get_agent_state()
            dup_state = copy.copy(state)
            action = agent.choose_action(state)
            is_terminal = domain.step(action)
            new_state = domain.get_agent_state()
            if not is_terminal:
                # if the game has not ended, incur a cost of living reward
                reward = -0.1
                agent.SR_learn(dup_state, action, reward, new_state)
                total_reward += reward
            else:
                if domain.reached_goal():
                    # if the game ended and agent is at the goal
                    reward = 0
                else:
                    # if max_steps is reached and agent not at goal
                    reward = -0.1
                total_reward += reward
                new_state = domain.get_agent_state()
                agent.SR_learn(dup_state, action, reward, new_state)
                agent_alive = False
        rewards.append(total_reward)
        episode += 1
    return rewards


def test(num_episodes, domain, agent, display, goal_index):

    for episode in range(num_episodes):
        total_reward = 0
        domain.reinitialize(goal_index)
        while True:
            full_state = domain.get_full_state()
            full_dup_state = copy.copy(full_state)
            display.update_grid(full_dup_state)

            state = domain.get_agent_state()
            dup_state = copy.copy(state)

            time.sleep(0.5)
            action = agent.choose_action(state)
            state_tup = tuple(state)
            is_terminal = domain.step(action)
            new_state = domain.get_full_state()
            for action in domain.possible_actions:
                print action
                print agent.get_Q(state, action)
                # print agent.m_table[(tuple(state), action)]
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
            display.update_grid(new_state)
            time.sleep(0.5)
        print "Episode: " + str(episode) + ", Total Reward: " + str(total_reward)
        display.end_game()
    return True

def parse_config(config_file):
    cfg = {}
    for line in config_file:
        key,value = line.strip().split(' = ')
        if key == 'initial_goal' or key == 'second_goal':
            x,y = int(value[1]), int(value[3])
            value = (x-1)*10-1+y
        cfg[key] = int(value)
    return cfg

def SASR_agent_run(run_number):

    goal_index = cfg['initial_goal']
    domain = MovingGoalsWorld(goal_index)
    agent = SASRagent(domain.possible_actions, goal_index)

    print '> STARTING LATENT LEARNING...'
    # training on default epsilon = 1 (pure exploration)
    train(cfg['max_explore_episodes'], domain, agent, goal_index)

    # seting the exploration rate to 0 (pure exploitation)
    agent.set_epilson(0.0)

    print '> STARTING TRAINING...'
    rewards = train(cfg['max_exploit_episodes'], domain, agent, goal_index)

    goal_index = cfg['second_goal']
    domain.set_goal(goal_index)
    agent.set_goal(goal_index)

    print '> STARTING SECOND GOAL TRAINING...'
    new_rewards = train(cfg['max_exploit_episodes2'], domain, agent, goal_index)

    return rewards, new_rewards


def plot_and_save(y, title):
    x = [i for i in range(len(y))]
    plt.plot(x, y)
    plt.savefig(title)
    plt.close()


if __name__ == '__main__':

    f = open('run.config', 'r')
    cfg = parse_config(f)

    total_runs = 6

    # train SASR agents in multiple processes
    pool = multiprocessing.Pool(total_runs)
    out = pool.map(SASR_agent_run, range(total_runs))

    # save plots for individual plots
    for run in range(total_runs):
        first_rewards, second_rewards = out[run]

        plot_and_save(first_rewards, 'first_goal_' + str(run+1))
        plot_and_save(second_rewards, 'second_goal_' + str(run+1))

    # compute averages across runs
    average_first_rewards = [0 for i in range(len(out[0][0]))]
    average_second_rewards = [0 for i in range(len(out[0][1]))]

    for run in range(total_runs):
        first_rewards, second_rewards = out[run] 
        average_first_rewards = map(add, average_first_rewards, first_rewards)
        average_second_rewards = map(add, average_second_rewards, second_rewards)

    average_first_rewards = map(div, average_first_rewards, [float(total_runs) for i in range(len(average_first_rewards))])
    average_second_rewards = map(div, average_second_rewards, [float(total_runs) for i in range(len(average_first_rewards))])

    # plot average rewards over time
    plot_and_save(average_first_rewards, 'average_first_goal')
    plot_and_save(average_second_rewards, 'average_second_goal')


    # while True:
    #     inp = raw_input('Enter test or quit: ')

    #     if inp == 'quit':
    #         break
    #     elif inp == 'test':
    #         display = visualize.VisualGame(domain.get_full_state())
    #         domain.reinitialize(goal_index)
    #         # state = domain.get_state()

    #         test_thread = threading.Thread(target = test, args = (1, domain, agent, display, goal_index))
    #         display_thread = threading.Thread(target = display.run)

    #         # so that we can exit from shell while thread is running
    #         test_thread.daemon = True
    #         display_thread.daemon = True

    #         test_thread.start()
    #         display_thread.start()
    #     else:
    #         continue
    