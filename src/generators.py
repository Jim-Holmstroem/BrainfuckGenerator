from __future__ import print_function
import numpy as np
import bf_interpreter as ip



def trivial_generate(output):
    """
    output - should be the string that you want to output
    """
    data = np.array([0]+map(ord, output))
    diff = np.diff(data)
    pm = map(lambda d: ("-","+")[d>0]*abs(d), diff)
    return ".".join(pm)+"."

def trivial_loop_generate(output):
    pass
