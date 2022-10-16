from errno import ECHILD
from .fullmodel import Ecosystem
import time

def findBetterInitP(ecosys: Ecosystem, ecoinit: Ecosystem) -> list[float]:
    recChanges: list[float] = [0.0 for _ in ecosys.allSpecies]
    ecosim = ecoinit.clone()
    extIndex = ecosys.extinction()
    while extIndex:
        for species in extIndex:
            for i, (key, value) in enumerate(ecoinit.allSpecies[species].depGrowthRate.items()):
                # if value > 0:
                #     ecosys.allSpecies[i].population += 0.05
                #     recChanges[i] += 0.05
                # if value < 0:
                #     ecosys.allSpecies[i].population -= 0.05
                #     recChanges[i] -= 0.05
                if value != 0:
                    recChanges[i] += 1.0 / value
            recChanges[species] += 1
        for i in range(len(ecosys.allSpecies)):
            ecosim.allSpecies[i].population = ecoinit.allSpecies[i].population + recChanges[i]
        ecosim.fullModel()
        extIndex = ecosim.extinction()
        ecosim = ecoinit.clone()

    return recChanges