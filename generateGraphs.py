import networkx as nx
import itertools
from st_fd import *
from bottleneck import *

def generate_lists(upper_bound, length, current_list=[]):
    if len(current_list) < length:
        for i in range(1,upper_bound+1):
            yield from generate_lists(upper_bound, length, current_list + [i])
    elif len(current_list) == length:
        yield current_list

def generatePathologicalList(weights):
    k = len(weights)
    F = sum(weights)
    # generate all subsets of the set {0,...,k-1}
    lst = []
    for length in range(1, int(k/2)+1):
        # print(f"length {length}")
        last_subsets_count = 0
        for subset in itertools.combinations(range(k),length):
            # print(subset)
            s = sum(weights[i] for i in subset)
            # print(s)
            # append to list the integer made up of summing up the weights of the indices in subset
            lst.append(s)
            last_subsets_count += 1
        # print(f"last_subsets_count {last_subsets_count}")
    if k % 2 == 0:
        # remove the last last_subsets_count/2 elements from lst
        lst = lst[:-int(last_subsets_count/2)]

    return lst

def generateGraphLines(lst, F):
    lines = []

    n = len(lst) + 1
    lines += [f"{n + len(lst)}"]
    for i in range(n-1):
        lines += [f"{i} {i+1} {lst[i]}"]
        lines += [f"{i} {i+len(lst)+1} {F - lst[i]}"]
        lines += [f"{i+len(lst)+1} {i+1} {F - lst[i]}"]

    return(lines)


def solveGreedy(weights):
    totF = sum(weights)
    lst = generatePathologicalList(weights)
    lines = generateGraphLines(lst, totF)

    graph = read_input_standard("", "int", lines)
    source = graph['source']
    sink = graph['sink']

    flowNetwork, flowDict = getInputForMaxBottleneck(graph)
    bottleneckPaths, bottleneckWeights = decomposeWithMaxBottleneck(flowNetwork, flowDict, source, sink)

    return bottleneckPaths, bottleneckWeights

def solveGreedyWithFirstWeight(firstWeight, k, T):
    
    maxDiff = 1
    maxDiffList = []

    for weights in itertools.combinations(range(1, T+1), k - 1):
        weights = [firstWeight] + list(weights)
        
        bottleneckPaths, bottleneckWeights = solveGreedy(weights)
        if len(bottleneckPaths) - len(weights) > maxDiff:
            maxDiff = len(bottleneckPaths) - len(weights)
            maxDiffList = [(maxDiff, weights, bottleneckWeights)]
        elif maxDiff > 0 and len(bottleneckPaths) - len(weights) == maxDiff:
            maxDiffList.append((maxDiff, weights, bottleneckWeights))

    return maxDiffList