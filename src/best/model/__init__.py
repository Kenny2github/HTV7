from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Biome:
    species: list[Species]

@dataclass
class Species:
    # reproduction rate
    # population(t+1) = population(t) * (1 + reproduction)
    reproduction: float
    # mapping of species it preys on to rate of eating
    prey: dict[Species, float]

@dataclass
class Ecosystem:
    # mapping of species to its population
    population: dict[Species, int]
