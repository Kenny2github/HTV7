from errno import ECHILD
from .fullmodel import Ecosystem
from .species import Species

def findBetterInitP(ecosys: Ecosystem) -> list[float]:
    recChanges: list[float] = [0.0 for _ in ecosys.allSpecies]
    extIndex = ecosys.extinction()
    while extIndex:
        for species in extIndex:
            for i, (key, value) in enumerate(ecosys.allSpecies[species].depGrowthRate.items()):
                # if value > 0:
                #     ecosys.allSpecies[i].population += 0.05
                #     recChanges[i] += 0.05
                # if value < 0:
                #     ecosys.allSpecies[i].population -= 0.05
                #     recChanges[i] -= 0.05
                if value != 0:
                    ecosys.allSpecies[i].population += 1 / value
                    recChanges[i] += 1 / value
            recChanges[species] += 1
        print(recChanges)
        extIndex = ecosys.extinction()

    return recChanges