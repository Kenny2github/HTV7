from dataclasses import dataclass, field
import os
from time import time
from typing import Union
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtWidgets import (
    QWidget, QComboBox, QGridLayout, QLabel, QTableView,
    QSlider, QPushButton, QMessageBox
)

from ..model.fullmodel import Ecosystem, load_ecosystem
from ..model.species import Species
from ..model.tweak import findBetterInitP
from .population_input import SpeciesDisplay
from .utils import QHLine
from ..model.recommendations import giveRecs

GIVE_UP_TIME = 1.0

@dataclass
class PredictionModel(QAbstractTableModel):
    species: list[str] = field(default_factory=list)
    predictions: list[float] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__init__()
        self.predictions[:] = [round(x, 3) for x in self.predictions]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> str:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ['Species', 'Predicted Population (1000s)',
                    'Recommended Adjustment (1000s)'][section]
        return super().headerData(section, orientation, role)

    def data(self, index: Union[QModelIndex, QPersistentModelIndex],
             role: int = ...) -> Union[str, None]:
        if role == Qt.ItemDataRole.DisplayRole:
            return str([self.species, self.predictions, self.recommendations
                        ][index.column()][index.row()])
        return None

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.species)

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return 3

class MainWidget(QWidget):

    ecosystems = {}
    for path in os.listdir('ecosystems'):
        if not path.endswith('.json'):
            continue
        system = load_ecosystem(f'ecosystems/{path}')
        ecosystems[system.name] = system

    try:
        del system, path
    except NameError:
        pass

    @property
    def selectedEcosystem(self) -> Ecosystem:
        return self.ecosystems[self.ecosystemSelect.currentText()]

    def __init__(self) -> None:
        super().__init__()

        self.ecosystemSelect = QComboBox()
        self.ecosystemSelect.addItems(list(self.ecosystems.keys()))
        self.ecosystemSelect.activated.connect(self.setPopulations) # type: ignore

        self.timeSlider = QSlider(Qt.Orientation.Horizontal)
        self.timeSlider.setMinimum(0)
        self.timeSlider.setMaximum(100)
        self.timeSlider.setToolTip('Greater values lag more')
        self.timeSlider.setValue(80)

        self.timeLabel = QLabel(f'{self.timeSlider.value()} steps')
        self.timeSlider.sliderMoved.connect( # type: ignore
            lambda value: self.timeLabel.setText(f'{value} steps'))

        self.resSlider = QSlider(Qt.Orientation.Horizontal)
        self.resSlider.setMinimum(1)
        self.resSlider.setMaximum(40001)
        self.resSlider.setToolTip('Greater values lag more')
        self.resSlider.setValue(4001)

        self.resLabel = QLabel(f'{self.resSlider.value()} steps')
        self.resSlider.sliderMoved.connect( # type: ignore
            lambda value: self.resLabel.setText(f'{value} steps'))

        self.simulateButton = QPushButton('Simulate!')
        self.simulateButton.setEnabled(False)
        self.simulateButton.clicked.connect(self.simulate) # type: ignore

        self.plotButton = QPushButton('Plot Population over Time')
        self.plotButton.setEnabled(False)
        self.plotButton.clicked.connect(self.plot) # type: ignore

        self.predictionView = QTableView()

        layout = QGridLayout(self)
        layout.addWidget(QLabel('Select biome:'), 0, 0)
        layout.addWidget(self.ecosystemSelect, 0, 1, 1, 2)
        layout.addWidget(QHLine(), 1, 0, 1, 3)
        layout.addWidget(QLabel('Timesteps:'), 2, 0)
        layout.addWidget(self.timeSlider, 2, 1)
        layout.addWidget(self.timeLabel, 2, 2)
        layout.addWidget(QLabel('Time resolution:'), 3, 0)
        layout.addWidget(self.resSlider, 3, 1)
        layout.addWidget(self.resLabel, 3, 2)
        layout.addWidget(self.simulateButton, 4, 0, 1, 2)
        layout.addWidget(self.plotButton, 4, 2)
        layout.addWidget(self.predictionView, 5, 0, 1, 3)
        self.setLayout(layout)

    def setPopulations(self) -> None:
        self.ecosystems[self.ecosystemSelect.currentText()] \
            = self.selectedEcosystem.clone()
        self.dialog = SpeciesDisplay(self.selectedEcosystem)
        self.dialog.exec()
        if self.dialog.result() == self.dialog.Accepted:
            self.simulateButton.setEnabled(True)
            self.plotButton.setEnabled(True)

    def simulate(self) -> None:
        timeSteps = self.timeSlider.value()
        resolution = self.resSlider.value()
        testEcosys = self.selectedEcosystem.clone()
        self.selectedEcosystem.fullModel(timeSteps, resolution)
        allSpecies = self.selectedEcosystem.allSpecies

        recommending = findBetterInitP(self.selectedEcosystem, testEcosys)
        start = time()
        for _ in recommending:
            if time() - start > GIVE_UP_TIME:
                recommending.send(True) # stop now
                QMessageBox.warning(self, 'Anti-Extinction Efforts Failed',
                                    'Failed to find a population change that '
                                    'prevents all extinctions. Recommendations '
                                    'may be nonsensical.')
                break
        recommendations = recommending.value
        self.predictionView.setModel(PredictionModel(
            [species.name for species in self.selectedEcosystem.allSpecies],
            [species.population for species in self.selectedEcosystem.allSpecies],
            [str(recommendations[species]) for species in allSpecies],
        ))
        self.predictionView.resizeColumnsToContents()

    def plot(self) -> None:
        import matplotlib.pyplot as plt
        from itertools import cycle
        if not self.selectedEcosystem.lastSimulation:
            self.simulate()
        for (i, population), color in zip(
            enumerate(self.selectedEcosystem.lastSimulation),
            cycle(['b-', 'r-', 'b--', 'r--', 'b.', 'r.'])
        ):
            plt.plot(self.selectedEcosystem.lastT, population, color, label=f'x{i}(t)')
        plt.title('Population over time')
        plt.ylabel('Populations')
        plt.xlabel('Time (decades)')
        plt.legend(loc='best')
        plt.show()
