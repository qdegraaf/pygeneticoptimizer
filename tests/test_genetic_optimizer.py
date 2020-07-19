# -*- coding: utf-8 -*-

import logging
import random
from typing import List

import optimizer
from optimizer.genetic_optimizer import GeneticOptimizer, LevenshteinOptimizer
from unittest.mock import Mock
import pytest


class FixedPopOptimizer(GeneticOptimizer):
    def _init_population(self) -> List[str]:
        return ["tesstring1", "tesstring2", "tesstring3", "tesstring4", "tesstring5"]


class TestGeneticOptimizer:
    def test_weighted_choice(self):
        initial_list = [("some string", 0.4), ("test string", 12), ("TEST TEST", 42)]
        random.seed(1)  # sets n in function to 7.309414879714626 with the above input
        assert GeneticOptimizer._weighted_choice(initial_list) == "test string"

    def test_random_mutate_changes_dna_on_1(self):
        dna = "a test string"
        opt = FixedPopOptimizer(dna, 5, 321, logging.getLogger("testlogger"))
        mock = Mock(return_value=0)
        optimizer.genetic_optimizer.random.randrange = mock
        res = opt._random_mutate(dna)
        assert res == dna
        mock = Mock(return_value=1)
        optimizer.genetic_optimizer.random.randrange = mock
        res = opt._random_mutate(dna)
        assert res != dna

    def test_levenshtein_fitness_is_one_for_matching_strings(self):
        lev_opt = LevenshteinOptimizer("equaltest", 12, 21, logging.getLogger("testlogger"))
        assert lev_opt._calculate_fitness("testequal", "testequal") == 1

    def test_levenshtein_fitness_is_larger_than_zero_smaller_than_one_for_none_matching_strings(self):
        lev_opt = LevenshteinOptimizer("unequal", 12, 21, logging.getLogger("testlogger"))
        assert 0 < lev_opt._calculate_fitness("unequal", "strings") < 1

    def test_unicode_fitness_is_one_for_matching_strings(self):
        uni_opt = GeneticOptimizer("equaltest", 12, 21, logging.getLogger("testlogger"))
        assert uni_opt._calculate_fitness("testequal", "testequal") == 1

    def test_unicode_fitness_is_larger_than_zero_smaller_than_one_for_none_matching_strings(self):
        uni_opt = GeneticOptimizer("unequal", 12, 21, logging.getLogger("testlogger"))
        assert 0 < uni_opt._calculate_fitness("unequal", "strings") < 1

    def test_crossover_returns_equal_sized_children(self):
        father, mother = "crossover1", "crossover2"
        uni_opt = GeneticOptimizer("crossoverX", 12, 21, logging.getLogger("testlogger"))
        child1, child2 = uni_opt._crossover(father, mother)
        assert len(child1) == len(child2) == len(father) == uni_opt.dna_size


if __name__ == "__main__":
    pytest.main([__file__])