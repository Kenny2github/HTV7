from collections import Counter
from .species import Species

EXTINCTION_THRESHOLD = 1.0e-3
OVERPOPULATION_THRESHOLD = 1.0e12

def saveSpecies(species: Species) -> Counter[Species]:
    if species.population >= EXTINCTION_THRESHOLD:
        return Counter()
    return Counter(
        {s: 1 if rate > 0 else -1 for s, rate in species.depGrowthRate.items()
         if rate != 0} | {species: 1}
    )

def preventOverpopulation(species: Species) -> Counter[Species]:
    if species.population < OVERPOPULATION_THRESHOLD:
        return Counter()
    return Counter({species: -10000000})

def giveRecs(species: Species) -> Counter[Species]:
    recs = saveSpecies(species)
    recs.update(preventOverpopulation(species))
    return recs
