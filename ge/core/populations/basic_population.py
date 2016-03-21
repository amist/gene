import random
import math
import statistics
import sys
from ..population import Population

class BasicPopulation(Population):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        