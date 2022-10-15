from __future__ import annotations
from dataclasses import dataclass

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

