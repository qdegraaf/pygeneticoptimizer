# -*- coding: utf-8 -*-
""" benchmark.py allows for acquiring data on multiple genetic optimization runs and storing them
    in easily analysable csv format. When run it will optimize for TARGET using all available
    optimization methods (currently supports Levenshtein distance and Unicode distance). It will do
    this ITERATIONS times for all sizes in POPULATION_SIZE with the optimizer set to stop after
    MAX_GENERATIONS. The parameters can be tweaked to your liking though note that this can
    significantly increase the amount of time benchmark needs. Particularly longer TARGET strings
    and higher population sizes have a strong effect on performance. The results of a benchmark will
    be stored in FILEPATH for easy post processing """
import logging

import itertools
import time

import pandas as pd

from optimizer.genetic_optimizer import GeneticOptimizer, LevenshteinOptimizer


FILEPATH = "benchmark_results.csv"
TARGET = "How many?"
MAX_GENERATIONS = 5000
POPULATION_SIZE = [10, 20, 50, 100]
ITERATIONS = 10


def main():
    errorlog = logging.getLogger()
    errorlog.setLevel(logging.ERROR)

    methods = [GeneticOptimizer, LevenshteinOptimizer]

    result_list = []
    for method, popsize in itertools.product(methods, POPULATION_SIZE):
        for _ in range(0, ITERATIONS):
            gen_opt = method(TARGET, popsize, MAX_GENERATIONS, errorlog)
            # running a manual clock here for the time as timeit module is finicky about returning
            # function results
            tstart = time.time()
            results = gen_opt.optimize()
            tend = time.time() - tstart
            result_list.append({'Method': method.__name__,
                                'Population Size': popsize,
                                'Target Reached?': results[0],
                                'Generations': results[1],
                                'Time': tend
                                })

    df = pd.DataFrame(result_list)
    df.to_csv(FILEPATH, index=False)


if __name__ == "__main__":
    main()