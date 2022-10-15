from dataclasses import dataclass
import numpy as np
from scipy.integrate import odeint

from species import Species

@dataclass
class Ecosystem:
    allSpecies: list[Species]
    #To add a species, we must enter its name, independent growth rate, dependent growth rate, and current population
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
        #model defines the ODE system
        def model(X, t):
            dXdt = [
                population * (species.indepGrowthRate + sum(
                    pop * species.depGrowthRate.get(prey, 0.0)
                    for pop, prey in zip(X, self.allSpecies)
                ))
                for population, species in zip(X, self.allSpecies)
            ]
            return dXdt

        # number of time points
        n = 40001

        # time points
        t = np.linspace(0,80,n)

        for i in range(1,n):
            # span for next time step
            tspan = [t[i-1],t[i]]
            # solve for next step
            z = odeint(model, [species.population for species in self.allSpecies], tspan)
            # next initial condition
            #z[0] is equal to
            for species, newP in zip(self.allSpecies, z[1]):
                species.population = newP
