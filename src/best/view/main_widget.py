from dataclasses import dataclass, field
from typing import Union
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtWidgets import (
    QWidget, QComboBox, QGridLayout, QLabel, QTableView
)

from ..model import Biome, Species
from .population_input import SpeciesDisplay
from .utils import QHLine

@dataclass
class PredictionModel(QAbstractTableModel):
    species: list[str] = field(default_factory=list)
    predictions: list[int] = field(default_factory=list)
    recommendations: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__init__()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> str:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ['Species', 'Predicted Population', 'Recommended Change'][section]
        return super().headerData(section, orientation, role)

    def data(self, index: Union[QModelIndex, QPersistentModelIndex],
             role: int = ...) -> Union[str, int, None]:
        if role == Qt.ItemDataRole.DisplayRole:
            return [self.species, self.predictions, self.recommendations
                    ][index.column()][index.row()]
        return None

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.species)

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return 3

class MainWidget(QWidget):

    species1 = Species('Species1', 10.0, {})
    species2 = Species('Species2', 10.0, {species1: 1.0})
    species1.prey[species2] = 1.0

    biomes = {
        'Test': Biome('Test', [species1, species2])
    }

    del species1, species2

    @property
    def selectedBiome(self) -> Biome:
        return self.biomes[self.biomeSelect.currentText()]

    def __init__(self) -> None:
        super().__init__()

        self.biomeSelect = QComboBox()
        self.biomeSelect.addItems(list(self.biomes.keys()))
        self.biomeSelect.activated.connect(self.setPopulations) # type: ignore

        self.predictionView = QTableView()

        layout = QGridLayout(self)
        layout.addWidget(QLabel('Select biome:'), 0, 0)
        layout.addWidget(self.biomeSelect, 0, 1)
        layout.addWidget(QHLine(), 1, 0, 1, 2)
        layout.addWidget(self.predictionView, 2, 0, 1, 2)
        self.setLayout(layout)

    def setPopulations(self) -> None:
        self.dialog = SpeciesDisplay(self.selectedBiome)
        self.dialog.accepted.connect(self.simulate) # type: ignore
        self.dialog.exec()

    def simulate(self) -> None:
        print('Would give results here')
        self.predictionView.setModel(PredictionModel(
            [species.name for species in self.selectedBiome.species],
            [species.population for species in self.selectedBiome.species],
            [0 for _ in self.selectedBiome.species],
        ))
        self.predictionView.resizeColumnsToContents()
