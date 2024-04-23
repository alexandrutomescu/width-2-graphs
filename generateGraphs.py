import networkx as nx
import itertools
from st_fd import *
from bottleneck import *

# From here: https://ics.uci.edu/~eppstein/PADS/IntegerPartitions.py
def fixed_length_partitions(n,L):
    """
    Integer partitions of n into L parts, in colex order.
    The algorithm follows Knuth v4 fasc3 p38 in rough outline;
    Knuth credits it to Hindenburg, 1779.
    """
    
    # guard against special cases
    if L == 0:
        if n == 0:
            yield []
        return
    if L == 1:
        if n > 0:
            yield [n]
        return
    if n < L:
        return

    partition = [n - L + 1] + (L-1)*[1]
    while True:
        yield partition
        if partition[0] - 1 > partition[1]:
            partition[0] -= 1
            partition[1] += 1
            continue
        j = 2
        s = partition[0] + partition[1] - 1
        while j < L and partition[j] >= partition[0] - 1:
            s += partition[j]
            j += 1
        if j >= L:
            return
        partition[j] = x = partition[j] + 1
        j -= 1
        while j > 0:
            partition[j] = x
            s -= x
            j -= 1
        partition[0] = s

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
    
    maxDiff = 2
    maxDiffList = []

    for weights in itertools.combinations(range(firstWeight+1, T+1), k - 1):
        weights = [firstWeight] + list(weights)
        
        bottleneckPaths, bottleneckWeights = solveGreedy(weights)
        if len(bottleneckPaths) - len(weights) > maxDiff:
            maxDiff = len(bottleneckPaths) - len(weights)
            maxDiffList = [(maxDiff, weights, bottleneckWeights)]
        elif maxDiff > 0 and len(bottleneckPaths) - len(weights) == maxDiff:
            maxDiffList.append((maxDiff, weights, bottleneckWeights))

    return maxDiffList

def solveGreedyWithFirstWeightIP(firstWeight, k, F):
    
    maxDiff = 0
    maxDiffList = []

    for weights in fixed_length_partitions(F - firstWeight, k - 1):
        weights = [firstWeight] + weights
        
        bottleneckPaths, bottleneckWeights = solveGreedy(weights)
        if len(bottleneckPaths) - len(weights) > maxDiff:
            maxDiff = len(bottleneckPaths) - len(weights)
            maxDiffList = [(maxDiff, weights, bottleneckWeights)]
            print(maxDiff, weights, bottleneckWeights)
        elif maxDiff > 0 and len(bottleneckPaths) - len(weights) == maxDiff:
            maxDiffList.append((maxDiff, weights, bottleneckWeights))
            print(weights, maxDiff)

    return maxDiffList