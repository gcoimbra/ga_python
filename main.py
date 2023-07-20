import os
from typing import List

import matplotlib.pyplot
import numpy
import pandas

import problems
import pso

os.system("rm *.png video.avi")
pandas.set_option('display.float_format', lambda x: '%.3f' % x)


def run_k(k: int, problem: problems.Problem):
    finalFitnesses: List[float] = []
    positions = []
    for i in range(k):
        print(i)
        solver = pso.PSO(problem)
        solver.solve()
        finalFitnesses.append(problem.objective(solver.groupBestPosition))
        positions.append(solver.groupBestPosition)
    print(problem.name)
    bestPosition = positions[finalFitnesses.index(min(finalFitnesses))]
    print(bestPosition)
    print(problem.restrictionValues(bestPosition))
    print(problem.restrictions(bestPosition))
    print(pandas.Series(finalFitnesses).describe())

    solver = pso.PSO(problem)
    solver.solve()
	
    # solver = pso.PSO(problem)
    # solver.movie(30, 1)


#solver = pso.PSO(problems.Vaso())
#solver.movie(100,4)
run_k(10, problems.Vaso())
