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

    def __eq__(self, other: Species) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        rates = {species.name: rate for species, rate in self.depGrowthRate.items()}
        return f'Species(name={self.name!r}, indepGrowthRate={self.indepGrowthRate!r}, depGrowthRate={rates!r}, population={self.population!r})'
