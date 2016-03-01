from domain import *
from old_agent import *

if __name__ == '__main__':
	domain = MovingGoalsWorld()
	agent = OldAgent(domain.possible_actions)

	num_episodes = 100
	for episode in range(num_episodes):
		while True:
			state = domain.state
			action = agent.choose_action(state)
			if domain.step(action):
				new_state = domain.state
				reward = -0.1
				agent.Q_learn(state, action, reward, new_state)
			else:
				new_state = domain.state
				reward = 20
				agent.Q_learn(state, action, reward, new_state)
				break
		print episode
		print agent.q_table




	