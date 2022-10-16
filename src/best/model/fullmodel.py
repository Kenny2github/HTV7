import json
from dataclasses import dataclass, field
from typing import TypedDict
import numpy as np
from scipy.integrate import odeint

from .species import Species

@dataclass
class Ecosystem:
    name: str
    allSpecies: list[Species]

    lastSimulation: list[np.ndarray] = field(init=False, default_factory=list)
    lastT: np.ndarray = field(init=False, default=np.array([]))

    #To add a species, we must enter its name, independent growth rate, dependent growth rate, and current population
    def addSpecies(self, name, indepGR = 0.0, depGR = dict(), population = 0.0):
        newSpecies = Species(name, indepGR, depGR, population)
        self.allSpecies.append(newSpecies)

    def fullModel(self, timesteps: int = 80, resolution: int = 40001):
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
        n = resolution

        # time points
        t = np.linspace(0, timesteps, n)

        # species population graph
        populations = [np.empty_like(t) for _ in self.allSpecies]
        for population, species in zip(populations, self.allSpecies):
            population[0] = species.population

        initialPopulations = [species.population for species in self.allSpecies]

        # for i in range(1, n):
        #     # span for next time step
        #     tspan = [t[i-1],t[i]]
        #     # solve for next step
        #     z = odeint(model, [population[i-1] for population in populations], tspan)
        #     # next initial condition
        #     #z[0] is equal to
        #     for population, newP in zip(populations, z[1]):
        #         population[i] = newP
        #     yield i
        z = odeint(model, initialPopulations, t)
        for population, newP in zip(populations, np.transpose(z)):
            population[1:] = newP[1:]

        for population, species in zip(populations, self.allSpecies):
            species.population = population[n-1]
        self.lastSimulation = populations
        self.lastT = t

    def extinction(self) -> list[int]:
        extIndex = []
        for i, trend in enumerate(self.lastSimulation):
            if min(trend) < 0.001:
                extIndex.append(i)
        return extIndex

    # def findOptimalInitP(self, timesteps: int = 80, resolution: int = 40001, var = None):
        # simEco = Ecosystem(self.name, self.allSpecies)
        
        # # generates full list of variations to apply to initialP if never done so before
        # if var == None:
        #     var = [[0.0 for _ in range(len(self.allSpecies))] for _ in range(3 ** len(self.allSpecies))]
        #     for i in range(len(self.allSpecies)):
        #         for j in range(3 ** len(self.allSpecies)):
        #             var[j][len(self.allSpecies) - 1 - i] = 0.0 if (j // (len(self.allSpecies) ** i)) % 3 == 0 else (-0.05 if (j // (len(self.allSpecies) ** i)) % 3 == 1 else 0.05)
        
        # for i in range(3 ** len(self.allSpecies)):
        #     extinct = False
        #     for j in range(len(self.allSpecies)):
        #         simEco.allSpecies[j].population += var[i][j]
        #     simEco.fullModel(timesteps, resolution)
        #     for trend in simEco.lastSimulation:
        #         if trend.min() < 0.001:
        #             extinct = True


        


class EcosystemJSON(TypedDict):
    name: str
    species_names: list[str]
    r: list[float]
    A: list[list[float]]

def load_ecosystem(filename: str) -> Ecosystem:
    with open(filename, 'r') as f:
        data: EcosystemJSON = json.load(f)
    species = [Species(name, ri, {}) for name, ri in zip(data['species_names'], data['r'])]
    for row, prey in zip(data['A'], species):
        for col, predator in zip(row, species):
            prey.depGrowthRate[predator] = col
    return Ecosystem(data['name'], species)
