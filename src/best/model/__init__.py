from __future__ import annotations
from dataclasses import dataclass

from .species import Species

@dataclass
class Biome:
    name: str
    species: list[Species]
