from domain import *
from old_agent import *
from SASR_agent import *
import copy
import visualize
import multiprocessing
import time
import simplejson

import numpy as np

def train(max_episodes, domain, agent, goal_index):
    chunk_size = 10
    rewards = []
    episode = 0
    while True:
        if episode % 10 == 0:
            # print 'explored states: ' + str(agent.explored_SA_count)
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
                agent.learn(dup_state, action, reward, new_state)
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
                agent.learn(dup_state, action, reward, new_state)
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
    domain = ToyWorld(goal_index)
    agent = SASRagent(domain.possible_actions, goal_index)

    print '> STARTING LATENT LEARNING...'
    # training on default epsilon = 1 (pure exploration)
    train(cfg['max_explore_episodes'], domain, agent, goal_index)

    # seting the exploration rate to 0 (pure exploitation)
    agent.set_epilson(0.0)

    print '> STARTING TRAINING...'
    first_rewards = train(cfg['max_exploit_episodes'], domain, agent, goal_index)

    goal_index = cfg['second_goal']
    domain.set_goal(goal_index)
    agent.set_goal(goal_index)

    print '> STARTING SECOND GOAL TRAINING...'
    second_rewards = train(cfg['max_exploit_episodes2'], domain, agent, goal_index)

    return first_rewards, second_rewards


def Q_agent_run(run_number):

    goal_index = cfg['initial_goal']
    domain = ToyWorld(goal_index)
    agent = OldAgent(domain.possible_actions)

    print '> STARTING LATENT LEARNING...'
    # training on default epsilon = 1 (pure exploration)
    train(cfg['max_explore_episodes'], domain, agent, goal_index)

    # seting the exploration rate to 0 (pure exploitation)
    agent.set_epilson(0.0)

    print '> STARTING TRAINING...'
    first_rewards = train(cfg['max_exploit_episodes'], domain, agent, goal_index)

    goal_index = cfg['second_goal']
    domain.set_goal(goal_index)

    print '> STARTING SECOND GOAL TRAINING...'
    second_rewards = train(cfg['max_exploit_episodes2'], domain, agent, goal_index)

    return first_rewards, second_rewards


def plot_and_save(y, title):
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

    x = [i for i in range(len(y))]
    plt.plot(x, y)
    plt.savefig(title)
    plt.close()

def save_results(results):
    # input: results is a list of (first_rewards, second_rewards) tuples
    # saves mean, std rewards per episode across the total runs
    first_rewards = np.array([results[i][0] for i in range(total_runs)])
    second_rewards = np.array([results[i][1] for i in range(total_runs)])

    std_arr1 = np.std(first_rewards, axis = 0, dtype = np.float64)
    mean_arr1 = np.mean(first_rewards, axis = 0, dtype = np.float64)

    std_arr2 = np.std(second_rewards, axis = 0, dtype = np.float64)
    mean_arr2 = np.mean(second_rewards, axis = 0, dtype = np.float64)

    outfile = open('avg1.txt', 'w')
    simplejson.dump(list(mean_arr1), outfile)
    outfile.close()

    outfile = open('std1.txt', 'w')
    simplejson.dump(list(std_arr1), outfile)
    outfile.close()

    outfile = open('avg2.txt', 'w')
    simplejson.dump(list(mean_arr2), outfile)
    outfile.close()

    outfile = open('std2.txt', 'w')
    simplejson.dump(list(std_arr2), outfile)
    outfile.close()

if __name__ == '__main__':

    f = open('run.config', 'r')
    cfg = parse_config(f)

    total_runs = 10
    
    pool = multiprocessing.Pool(total_runs)

    # # train SASR agents in multiple processes
    out = pool.map(SASR_agent_run, range(total_runs))

    # train Q-learning agents in multiple processes
    # out = pool.map(Q_agent_run, range(total_runs))

    save_results(out)

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
    