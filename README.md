Extends succesor represention idea in http://www.gatsby.ucl.ac.uk/~dayan/papers/sr93.pdf to estimate Q-values using state-action successor representations.

Currently, the code successfully runs traditional Q-learning (Watkins, 1989) on the MovingGoalsWorld domain, which is specified in world.txt file. In this environment, a goal is chosen randomly at each episode among the locations marked with a 'g'.


Requirements:
* pygame
* threading
* numpy

TODO:
* debug SASR_agent.py that builds a state-action successor representation table to calculate Q values.
