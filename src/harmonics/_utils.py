import os
import yaml
import numpy as np
import time


def timer(string, t):
    print(f"{string} took {time.time() - t} seconds")
    return time.time()

def _list(thing):
    if type(thing) in (tuple, list, np.ndarray):
        return thing
    if type(thing) in (str, float, str):
        return [thing]
