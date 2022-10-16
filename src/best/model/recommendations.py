import json
from dataclasses import dataclass, field
from typing import TypedDict
import numpy as np
from scipy.integrate import odeint
from .species import Species
from fullmodel import Ecosystem

def giveRecs(S: Species, threshold:int, Eco: Ecosystem):
    preds = []
    preys = []
    if(S.population<threshold):
        for s in S.depGrowthRate:
            if (S.depGrowthRate[s] < 0):
                preds = preds + s
            if(S.depGrowthRate[s] >0):
                preys= preys+s
    Rec = "Import/ breed/ feed the preys:" + [x for x in preys] + "and/or remove predsators:" + [y for y in preds]
    return Rec

