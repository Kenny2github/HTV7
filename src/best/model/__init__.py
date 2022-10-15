from __future__ import annotations
from dataclasses import dataclass

from species import Species

@dataclass
class Biome:
    name: str
    species: list[Species]

@dataclass
class Species:
    name: str
    # reproduction rate
    # population(t+1) = population(t) * (1 + reproduction)
    reproduction: float
    # mapping of species it preys on to rate of eating
    prey: dict[Species, float]

    population: int = 0

    def __eq__(self, other: Species) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

@dataclass
class Ecosystem:
    # mapping of species to its population
    population: dict[Species, int]
