Extends succesor represention idea in http://www.gatsby.ucl.ac.uk/~dayan/papers/sr93.pdf to estimate Q-values using state-action successor representations. Currently tested in tabular form in the custom ToyWorld domain. Stay tuned for generalized version on Facebook's MazeBase domains!

#Files:
old_agent.py is a traditional Q-learning (Watkins, 1989) agent and SASR_agent.py is the state-action successor representation agent. These can be tested on the ToyWorld (specified in domain.py), and configured with world.txt file. The main file is run.py, which can be modified for different experiments, along with run.config. After running experiments and generating mean and standard deviation data, run plot_results.py to visualize the results.

#Requirements:
* pygame
* threading
* numpy
* multiprocessing
* matplotlib
* plotly

#Todo:
* Create a predicted future occupancy map for visualization (Dayan, 1993)
* Bonus: extend the current code to support linear function approximation for SASR (?)