from .species import Species
from .fullmodel import Ecosystem

def giveRecs(S: Species, threshold:int, Eco: Ecosystem):
    preds = []
    preys = []
    if(S.population<threshold):
        for s, rate in S.depGrowthRate.items():
            if (rate < 0):
                preds = preds + s
            if(rate >0):
                preys= preys+s
    Rec = "Import/ breed/ feed the preys:" + [x for x in preys] + "and/or remove predsators:" + [y for y in preds]
    return Rec

