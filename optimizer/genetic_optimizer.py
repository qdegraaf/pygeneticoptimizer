# -*- coding: utf-8 -*-
import logging
import random
from typing import List, Tuple, Callable


class GeneticOptimizer:
    """
    GeneticOptimizer is a base class for genetic optimizers handling general functionality
    such as random mutation, creation of offspring, as well as a basic unicode optimization method
    """
    def __init__(self, target: str, population_size: int, max_generations: int,
                 logger: logging.Logger):
        self.target_fitness = float
        self.weighted_population = List[Tuple[str, float]]
        self.target = target
        self.dna_size = len(self.target)
        self.population_size = population_size
        self.population = self._init_population()
        self.max_generations = max_generations
        self.logger = logger

    def _init_population(self) -> List[str]:
        """
        return a random initial population of size population_size with inhabitants of length
        dna_size
        """
        pop = []
        for i in range(self.population_size):
            dna = ""
            for c in range(self.dna_size):
                dna += self._random_char()
            pop.append(dna)
        return pop

    def _random_mutate(self, dna: str) -> str:
        """ randomly mutate a character to ensure genepool diversity and reduce risk of getting
        stuck in local minima/maxima """
        result = ""
        for c in range(self.dna_size):
            if random.randrange(0, 100, 1) == 1:
                result += self._random_char()
            else:
                result += dna[c]
        return result

    @staticmethod
    def _random_char() -> str:
        """
        Return a random printable character between ASCII decimal 32 and 126
        """
        return chr(int(random.randrange(32, 126, 1)))

    def _crossover(self, mother: str, father: str) -> Tuple[str, str]:
        """create two child genes from a mother and father gene"""
        position = random.randrange(0, self.dna_size, 1)
        return mother[:position] + father[position:], father[:position] + mother[position:]

    @staticmethod
    def _weighted_choice(items: List[Tuple[str, float]]) -> str:
        """ choose a random element from the items list with a probability associated with its
            weight """
        total_weight = sum(item[1] for item in items)
        n = random.uniform(0, total_weight)
        for item, weight in items:
            if weight > n:
                return item
            n -= weight

    def optimize(self) -> Tuple[bool, int]:
        """approach target through genetic optimization"""
        self.weighted_population = self._weigh_population(self._calculate_fitness)
        self.target_fitness = self._calculate_fitness(self.target, self.target)

        for gen in range(self.max_generations):
            # Clear population as we will repopulate a new one
            self.population.clear()
            for _ in range(int(self.population_size / 2)):
                dna_1 = self._weighted_choice(self.weighted_population)
                dna_2 = self._weighted_choice(self.weighted_population)

                dna_1 = self._random_mutate(dna_1)
                dna_2 = self._random_mutate(dna_2)

                dna_1, dna_2 = self._crossover(dna_1, dna_2)
                self.population.extend([dna_1, dna_2])
            self.weighted_population.clear()

            fittest = ("", 0)
            for dna in self.population:
                fitness = self._calculate_fitness(dna, self.target)
                self.weighted_population.append((dna, fitness))
                if fitness > fittest[1]:
                    fittest = (dna, fitness)
                    if fitness == self.target_fitness:
                        self.logger.info(f"Target '{fittest[0]}' reached in {gen} generations ")
                        return True, gen
            if gen % 10 == 0:
                self.logger.info(f"Fittest candidate after {gen} generations = {fittest[0]} "
                                 f"with a fitness of {fittest[1]}")

        self.logger.info(f"target was not reached after {self.max_generations} generations,"
                         f" stopping optimizer")
        return False, self.max_generations

    def _weigh_population(self,
                          fitness_function: Callable[[str, str], float]) -> List[Tuple[str, float]]:
        """add weights to all dna in population"""
        weighted_population = []
        for dna in self.population:
            weight = fitness_function(dna, self.target)
            weighted_population.append((dna, weight))
        return weighted_population

    def _calculate_fitness(self, dna: str, target: str) -> float:
        """ define a fitness function as being the sum of the unicode distances of the characters
        of a chosen string to a target string
        make minimum fitness 1 to avoid possible division by zero later """
        fitness = 1
        for c in range(self.dna_size):
            fitness += abs(ord(dna[c]) - ord(target[c]))
        return 1 / fitness


class LevenshteinOptimizer(GeneticOptimizer):
    """A genetic optimizer which uses the levenshtein distance between the target string and a
     population member to calculate its fitness"""
    def _calculate_fitness(self, dna: str, target: str) -> float:
        """ return a fitness based on the levensthein distance of a chosen string to a
        target string
        make minimum fitness 1 to avoid possible division by zero later """
        fitness = 1 + self._levenshtein(dna, target)
        return 1 / fitness

    @staticmethod
    def _levenshtein(startstring: str, targetstring: str,
                     costs: Tuple[int, int, int] = (1, 1, 1)) -> int:
        """
            return the Levenshtein distance between the strings startstring and
            targetstring
            For all i and j, dist[i,j] will contain the Levenshtein
            distance between the first i characters of s and the
            first j characters of t

            costs: a tuple or a list with three integers (d, i, s)
                   where d defines the costs for a deletion
                         i defines the costs for an insertion and
                         s defines the costs for a substitution
        """

        rows = len(startstring) + 1
        cols = len(targetstring) + 1
        deletes, inserts, substitutes = costs

        dist = [[0 for _ in range(cols)] for _ in range(rows)]

        # source prefixes can be transformed into empty strings
        # by deletions:
        for row in range(1, rows):
            dist[row][0] = row * deletes

        # target prefixes can be created from an empty source string
        # by inserting the characters
        for col in range(1, cols):
            dist[0][col] = col * inserts

        for col in range(1, cols):
            for row in range(1, rows):
                if startstring[row - 1] == targetstring[col - 1]:
                    cost = 0
                else:
                    cost = substitutes
                dist[row][col] = min(dist[row - 1][col] + deletes,
                                     dist[row][col - 1] + inserts,
                                     dist[row - 1][col - 1] + cost)  # substitution

        return dist[row][col]