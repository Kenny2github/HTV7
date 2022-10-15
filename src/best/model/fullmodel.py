from dataclasses import dataclass
import numpy as np
from scipy.integrate import odeint

from species import Species

@dataclass
class Ecosystem:
    allSpecies: list[Species]

    def addSpecies(self, name, indepGR = 0.0, depGR = dict(), population = 0.0):
        newSpecies = Species(name, indepGR, depGR, population)
        self.allSpecies.append(newSpecies)

    def fullModel(self):
        r = np.matrix([
            [animal.indepGrowthRate] for animal in self.allSpecies
        ])

        A = np.matrix([
            [animal.depGrowthRate[key] for key in animal.depGrowthRate]
            for animal in self.allSpecies
        ])

        def model(self, X: list[Species], t):
            dXdt = [animal.totalRate() for animal in X]
            return dXdt
        
        # number of time points
        n = 40001

        # time points
        t = np.linspace(0,80,n)

        for i in range(1,n):
            # span for next time step
            tspan = [t[i-1],t[i]]
            # solve for next step
            z = odeint(model, self.allSpecies, tspan)
            # next initial condition
            for i, newP in enumerate(z[1]):
                self.allSpecies[i].population = newP