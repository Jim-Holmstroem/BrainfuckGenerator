from __future__ import print_function
import numpy as np


#Genetic operatorions
def crossover(program_a, program_b, ncrossovers = 2):
    """
    
    returns a crossover and it's complement
    """

    crossovers_a = np.shuffle(len(program_a))[:ncrossovers].sort() #TODO chance to np.choice instead
    crossovers_b = np.shuffle(len(program_b))[:ncrossovers].sort() #TODO chance to np.choice instead
    #NOTE different crossoverpoints makes it possible to change length even without the mutations.

    pass

def mutate(program_a):
    """
    returns a mutation of program_a
    """
    pass

