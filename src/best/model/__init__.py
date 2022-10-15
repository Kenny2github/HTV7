from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Biome:
    species: list[Species]
    naturalDisasters: list[NaturalDisaster]

@dataclass
class NaturalDisaster:
    name: str
    occuranceRate: float
    effectOnSpecies: dict[Species, float]

@dataclass
class Species:
    name: str
    # reproduction rate
    # population(t + 1) = population(t) * (1 + reproduction) * (1 - death)
    reproduction: float
    natDeath: float
    # mapping of species it preys on to rate of eating
    consumationRate: float
    prey: dict[Species, float]
    
    population: int = 0
