import sys
import argparse
import math
import os
from st_fd import *
from bottleneck import *
from generateGraphs import *

parser = argparse.ArgumentParser(
    description="""
    Decompose a network flow into a minimum number of weighted paths. 
    This script uses the Gurobi ILP solver.
    """,
    formatter_class=argparse.RawTextHelpFormatter
    )

# multiplier
M = 162 

# lst is the list of flow values on one edge of each bubble
lst = [13,27,46,40,59,73,86]
lst = lst + [x*M for x in lst]

#flow value
totF = M ** 2 + 76 + 86

# generating a graph object from the list of flow values
lines = generateGraphLines(lst, totF)
graph = read_input_standard("", "int", lines)
source = graph['source']
sink = graph['sink']

# running the greedy algorithm
flowNetwork, flowDict = getInputForMaxBottleneck(graph)
bottleneckPaths, bottleneckWeights = decomposeWithMaxBottleneck(flowNetwork, flowDict, source, sink)

print(f"number of greedy paths: {len(bottleneckWeights)}")
print(f"greedy weights: {bottleneckWeights}")
assert(sum(bottleneckWeights) == totF)


    
    
        
