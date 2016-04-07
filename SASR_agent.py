import random
import numpy as np
from collections import OrderedDict

class SASRagent:
    def __init__(self, possible_actions, goal_index, gamma = 1, epsilon = 1.0, alpha = 0.9, default_Q = 0.0):
        """
        gamma: discount rate
        epsilon: exploration rate
        alpha: learning rate
        default_Q: default Q value
        possible_actions: list of possible actions
        """
        # m_table maps (state,action) to [SR, R]
        # where R is the immediate reward of taking action at state
        self.m_table = OrderedDict()
        self.explored_SA_count = 0
        self.gamma = gamma
        self.epsilon = epsilon
        self.alpha = alpha
        self.default_Q = default_Q
        self.actions = possible_actions
        self.goal_index = goal_index

    def set_goal(self, goal_index):
        self.goal_index = goal_index

    def reward(self, state):
        # 2 = GOAL
        # if the goal is still in the state, return cost of living
        if state != self.goal_index:
            return -0.1
        # else return reward of reaching the goal
        return 0

    def new_SA_update(self, state, action):
        # updates that need to be made when agent encounters new (state,action)
        self.m_table[(state, action)] = [self.get_default_SR(), self.reward(state)]
        for SR,_ in self.m_table.values():
            SR.append(0)
        self.explored_SA_count += 1

    def get_default_SR(self):
        return [0 for SA in range(self.explored_SA_count)]

    def set_epilson(self, new_epsilon):
        self.epsilon = new_epsilon

    def get_R_table(self):
        # returns a list of immediate rewards at all the explored states
        return np.array([elem[1] for elem in self.m_table.values()])

    def get_Q(self, state, action):
        if (state,action) in self.m_table:
            return np.dot(np.array(self.m_table[(state,action)][0]), self.get_R_table())
        else:
            return self.default_Q

    def choose_action(self, state):
        # epsilon greedy approach: choose randomly with probability epsilon
        if random.random()<self.epsilon:
            action = random.choice(self.actions)
        else:
            action = self.choose_optimal_action(state)
        return action

    # TODO: optimize this
    def choose_optimal_action(self, state):
        q_values = [self.get_Q(state, action) for action in self.actions]
        max_value = max(q_values)
        max_indices = [i for i, j in enumerate(q_values) if j == max_value]
        action = self.actions[random.choice(max_indices)]
        return action


    # TODO: optimize this with numpy(?)
    def learn(self, state, action, reward, new_state):

        # if we haven't already explored this state
        # then initialize it as a new state
        if (state, action) not in self.m_table:
            self.new_SA_update(state, action)
        
        # i = self.m_table.keys().index((state,action))
        new_action = self.choose_optimal_action(new_state)

        try:
            SR_new_state = self.m_table[(new_state,new_action)][0]
        except:
            self.new_SA_update(new_state, new_action)
            SR_new_state = self.m_table[(new_state,new_action)][0]
            # M_j is M(s_t, a_t)_j

        SR_state = self.m_table[(state,action)][0]
        for j, M_j in enumerate(SR_state):
            jth_state_tuple = self.m_table.keys()[j][0]
            SR_state[j] += self.alpha * (int(state == jth_state_tuple) + self.gamma * SR_new_state[j] - M_j)

        self.m_table[(state,action)][0] = SR_state

        # update reward
        self.m_table[(state,action)][1] = self.reward(state)


