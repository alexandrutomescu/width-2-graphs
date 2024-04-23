import sys
import argparse
import math
import os
from st_fd import *
from bottleneck import *
from generateGraphs import *
from itertools import permutations
import multiprocessing

parser = argparse.ArgumentParser(
    description="""
    Decompose a network flow into a minimum number of weighted paths. 
    This script uses the Gurobi ILP solver.
    """,
    formatter_class=argparse.RawTextHelpFormatter
    )
parser.add_argument('-t', '--threads', type=int, default=0, help='Number of threads to use for the Gurobi solver; use 0 for all threads (default 0).')

requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-k', '--k', type=int, help='Number of paths', required=True)
requiredNamed.add_argument('-m', '--max', type=int, help='max value of a path weight', required=False)
requiredNamed.add_argument('-f', '--flow', type=int, help='flow value (sum of path weights)', required=False)
requiredNamed.add_argument('-o', '--output', type=str, help='Output filename', required=True)


args = parser.parse_args()

threads = args.threads
if threads == 0:
    threads = os.cpu_count()
print(f"INFO: Using {threads} threads")

k = args.k
T = args.max
F = args.flow

log_file = args.output.split('.')[0] + '.log'

if __name__ == '__main__':
    pool = multiprocessing.Pool(threads)
    results = []
    for firstWeight in range(1, F):
        result = pool.apply_async(solveGreedyWithFirstWeightIP, (firstWeight, k, F, log_file))
        results.append(result)
    
    pool.close()
    pool.join()

    # Process the results
    for result in results:
        # append result to file names args.output
        result_str = '\n'.join(map(str,result.get()))
        try:
            with open(args.output, 'a') as file:
                file.write((result_str) + '\n')
        except FileNotFoundError:
            with open(args.output, 'w') as file:
                file.write((result_str) + '\n')

    

    
    
        
