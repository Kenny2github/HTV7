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

        z = odeint(model, initialPopulations, t)
        for population, newP in zip(populations, np.transpose(z)):
            population[1:] = newP[1:]

        for population, species in zip(populations, self.allSpecies):
            species.population = population[n-1]
        self.lastSimulation = populations
        self.lastT = t

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
