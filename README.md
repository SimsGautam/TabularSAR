Extends succesor represention idea in http://www.gatsby.ucl.ac.uk/~dayan/papers/sr93.pdf to estimate Q-values using state-action successor representations.

Currently, the code successfully runs traditional Q-learning (Watkins, 1989) on the MovingGoalsWorld domain, which is specified in world.txt file. In this environment, a goal is chosen randomly at each episode among the locations marked with a 'g'.


Requirements:
* pygame
* threading
* numpy

TODO:
* Create a predicted future occupancy heat map to visualize
* clean up run.py
* Implement linear function approximation for SASR

The linear function approximation would be useful because we could set up an experiment where we train the agent on a particular goal, then change the goal and measure the convergence rate of the approximate SASR of the new goal.