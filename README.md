Extends succesor represention idea in http://www.gatsby.ucl.ac.uk/~dayan/papers/sr93.pdf to estimate Q-values using state-action successor representations.

#Files:
old_agent.py is a traditional Q-learning (Watkins, 1989) agent and SASR_agent.py is the state-action successor representation agent. These can be tested on the MovingGoalsWorld (specified in domain.py), and configured with world.txt file. The main file is run.py, which can be modified for different experiments.

#Requirements:
* pygame
* threading
* numpy
* visualize
* multiprocessing
* matplotlib

#Todo:
* Create a predicted future occupancy map for visualization (Dayan, 1993)
* Bonus: extend the current code to support linear function approximation for SASR (?)

The linear function approximation would be useful because we could set up an experiment where we train the agent on a particular goal, then change the goal and measure the convergence rate of the approximate SASR of the new goal.