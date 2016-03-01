import random
import numpy as np

class OldAgent:
	def __init__(self, possible_actions, gamma = 0.9, epsilon = 0.1, alpha = 0.2, default_Q = 0.0):
		"""
		gamma: discount rate
		epsilon: exploration rate
		alpha: learning rate
		default_Q: default Q value
		possible_actions: list of possible actions
		"""
		self.q_table = {}
		self.gamma = gamma
		self.epsilon = epsilon
		self.alpha = alpha
		self.default_Q = default_Q
		self.actions = possible_actions

	def get_Q(self, state, action):
		state = tuple(state)
		return self.q_table.get((state,action), self.default_Q)

	def update_Q(self, new_estimate, state, action):
		# should update the Q-value in the table based on learning rate
		state = tuple(state)
		old_Q = self.q_table.get((state, action), None)
		if old_Q == None:
			self.q_table[(state, action)] = new_estimate
		else:
			self.q_table[(state, action)] = old_Q + self.alpha*(new_estimate - old_Q)

	def choose_action(self, state):
		# epsilon greedy approach: choose randomly with probability epsilon
		if random.random()<self.epsilon:
			action = random.choice(self.actions)
		else:
			q_values = np.array([self.get_Q(state, action) for action in self.actions])
			action = self.actions[np.argmax(q_values)]
		return action

	def Q_learn(self, state, action, reward, new_state):
		new_max_Q = max([self.get_Q(new_state,action) for action in self.actions])
		new_estimate = reward + self.gamma * new_max_Q
		self.update_Q(new_estimate, state, action)
