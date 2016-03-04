import random
import numpy as np
from collections import OrderedDict

class SASRagent:
    def __init__(self, possible_actions, gamma = 0.9, epsilon = 1, alpha = 0.2, default_Q = 0.0):
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

    def reward(self, state):
        # 2 = GOAL
        # if the goal is still in the state, return cost of living
        if 2 in state:
            return -0.1
        # else return reward of reaching the goal
        print "Reached GOAL"
        print state
        return 0

    def new_SA_update(self, state, action):
        #updates that need to be made when agent encounters new (state,action)
        state_tup = tuple(state)
        self.explored_SA_count += 1
        self.m_table[(state_tup, action)] = [self.get_default_SR(), self.reward(state)]
        for SR,_ in self.m_table.values():
            SR.append(0)

    def get_default_SR(self):
        return [0 for SA in range(self.explored_SA_count)]

    def set_epilson(self, new_epsilon):
        self.epsilon = new_epsilon

    def get_R_table(self):
        # returns a list of immediate rewards at all the explored states
        return np.array([elem[1] for elem in self.m_table.keys()])

    def get_Q(self, state, action):
        state_tup = tuple(state)
        try:
            return np.dot(self.m_table[(state_tup,action)][0], self.get_R_table())
        except:
            return self.default_Q

    def choose_action(self, state):
        # epsilon greedy approach: choose randomly with probability epsilon
        if random.random()<self.epsilon:
            action = random.choice(self.actions)
        else:
            q_values = [self.get_Q(state, action) for action in self.actions]
            max_value = max(q_values)
            max_indices = [i for i, j in enumerate(q_values) if j == max_value]
            action = self.actions[random.choice(max_indices)]
        return action

    def SR_learn(self, state, action, reward, new_state):

        state_tup = tuple(state)
        new_state_tup = tuple(new_state)
        new_action = self.choose_action(new_state)

        # if we haven't already explored this state
        if (state_tup, action) not in self.m_table:
            self.new_SA_update(state, action)
        
        i = self.m_table.keys().index((state_tup,action))
        try:
            SR_new_state = self.m_table[(new_state_tup,new_action)][0]
        except:
            SR_new_state = self.get_default_SR() + [0]
            # M_j is M(s_t, a_t)_j
        for j, M_j in enumerate(self.m_table[(state_tup,action)][0]):
            M_j += self.alpha * (int(i==j) + self.gamma * SR_new_state[j] - M_j)


