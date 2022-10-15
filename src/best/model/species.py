from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Species:
    name: str
    # growth rate of the population ignoring the effect of all other species in the biome
    indepGrowthRate: float
    # mapping of how other species affect the population
    depGrowthRate: dict[Species, float]
    # population in terms of thousands
    population: float = 0.0

    # an implimentation of the Lotka-Volterra model
    def model(self, X: list, t):
        dXdt = self.population * (self.indepGrowthRate + sum(key.population * self.depGrowthRate[key] for key in self.depGrowthRate))
        return dXdt