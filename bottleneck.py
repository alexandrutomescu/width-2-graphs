from itertools import count
import networkx as nx
import copy

bigNumber = 1 << 32

def maxBottleckPath(flowNetwork, flowDict, source, sink):
    B = dict()
    maxInNeighbor = dict()

    # Computing the B values with DP
    for v in nx.topological_sort(flowNetwork):
        if v == source:
            B[v] = bigNumber
        else:
            B[v] = -bigNumber
            for u in flowNetwork.predecessors(v):
                uBottleneck = min(B[u], flowDict[u][v])
                if uBottleneck > B[v]:
                    B[v] = uBottleneck 
                    maxInNeighbor[v] = u
    
    # If no s-t flow exists in the network
    if B[sink] == 0:
        return None, None
    
    # Recovering the path of maximum bottleneck
    reverse_path = [sink]
    while reverse_path[-1] != source:
        reverse_path.append(maxInNeighbor[reverse_path[-1]])
    
    return B[sink], list(reversed(reverse_path))

def decomposeWithMaxBottleneck(flowNetwork, flowDict, source, sink):
    pathDecomposition = list()
    pathWeights = list()
    # Making a copy of flowDict, otherwise the changes we make in this function 
    # will carry over to the global variable flowDict
    tempFlow = copy.deepcopy(flowDict)

    while True:
        bottleneck, path = maxBottleckPath(flowNetwork, tempFlow, source, sink)
        if path is None:
            break
            
        for i in range(len(path)-1):
            tempFlow[path[i]][path[i+1]] -= bottleneck
        
        pathDecomposition.append(path)
        pathWeights.append(bottleneck)
        
    return pathDecomposition, pathWeights


def getInputForMaxBottleneck(graph):
    edges = graph['edges']
    vertices = graph['vertices']
    in_neighbors = graph['in_neighbors']
    out_neighbors = graph['out_neighbors']

    flowNetwork = nx.DiGraph()
    flowDict = dict()

    # We add a corresponding to each node and initialize flowdict
    for v in vertices:
        flowNetwork.add_node(v)
        flowDict[v] = dict()
    # This enumerates through the dictionary edges:
    for (u, v), edge_value in edges.items():
        flowDict[u][v] = edge_value
        flowNetwork.add_edge(u, v)

    return flowNetwork, flowDict