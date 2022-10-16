from typing import Generator, Generic, TypeVar, Union
from .fullmodel import Ecosystem
from .species import Species

YT = TypeVar('YT')
ST = TypeVar('ST')
RT = TypeVar('RT')

class ValueStoringGenerator(Generic[YT, ST, RT]):
    gen: Generator[YT, ST, RT]
    value: RT

    def __init__(self, gen: Generator[YT, ST, RT]):
        self.gen = gen

    def __iter__(self) -> Generator[YT, ST, RT]:
        self.value = yield from self.gen
        return self.value

    def send(self, value: ST) -> Union[YT, RT]:
        try:
            return self.gen.send(value)
        except StopIteration as exc:
            self.value = exc.value
            return self.value

def _findBetterInitP(ecosys: Ecosystem, ecoinit: Ecosystem
                    ) -> Generator[int, bool, dict[Species, float]]:
    recChanges = {species: 0.0 for species in ecosys.allSpecies}
    ecosim = ecoinit.clone()
    extinctions = ecosys.extinctions()
    yield len(extinctions)
    while extinctions:
        for species in extinctions:
            for key, value in species.depGrowthRate.items():
                if value != 0:
                    recChanges[key] += 1.0 / value
            recChanges[species] += 1
        for simspecies, initspecies in zip(ecosim.allSpecies, ecoinit.allSpecies):
            simspecies.population = initspecies.population + recChanges[initspecies]
        ecosim.fullModel()
        extinctions = ecosim.extinctions()
        for simspecies, initspecies in zip(ecosim.allSpecies, ecoinit.allSpecies):
            simspecies.population = initspecies.population
        if (yield len(extinctions)):
            return recChanges

    return recChanges

def findBetterInitP(ecosys: Ecosystem, ecoinit: Ecosystem
                    ) -> ValueStoringGenerator[int, bool, dict[Species, float]]:
    return ValueStoringGenerator(_findBetterInitP(ecosys, ecoinit))
