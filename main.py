# -*- coding: utf-8 -*-
import logging
import sys
from argparse import ArgumentParser
from typing import Union

from argparse_utils.types import int_ge_two, int_ge_zero
from optimizer.genetic_optimizer import GeneticOptimizer, LevenshteinOptimizer


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-t', '--target',
        type=str,
        help="Target string to optimize for",
        required=True
    )
    parser.add_argument(
        '-m', '--method',
        type=str,
        help="method to use for optimizing currently supports levenshtein and unicode methods "
             "defaults to unicode",
        default="unicode",
        choices=["unicode", "levenshtein"]
    )
    parser.add_argument(
        '-p', '--population_size',
        type=int_ge_two,
        help="size of population to be kept. has to be at least two, defaults to 200",
        default=200
    )
    parser.add_argument(
        '-g', '--max_generations',
        type=int_ge_zero,
        help="maximum amount of generations the optimizer will be run for, default is 1000",
        default=1000
    )

    args = parser.parse_args()
    logger = setup_logger(logging.INFO)

    optimizer_methods = {
        "unicode": GeneticOptimizer,
        "levenshtein": LevenshteinOptimizer
    }

    genalg = optimizer_methods[args.method](target=args.target,
                                            population_size=args.population_size,
                                            max_generations=args.max_generations,
                                            logger=logger)
    genalg.optimize()


def setup_logger(loglevel: Union[int, str]) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(loglevel)
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format, '%Y-%m-%d %H:%M:%S%z')

    conh1 = logging.StreamHandler(sys.stdout)
    conh1.setLevel(logging.INFO)
    conh1.setFormatter(formatter)
    logger.addHandler(conh1)

    conh2 = logging.FileHandler("optimizerlogs", "a")
    conh2.setLevel(logging.DEBUG)
    conh2.setFormatter(formatter)
    logger.addHandler(conh2)
    return logger


if __name__ == "__main__":
    main()
