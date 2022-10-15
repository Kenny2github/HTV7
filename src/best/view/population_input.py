from typing import Union
from dataclasses import dataclass, field
from PySide6.QtCore import (
    QAbstractItemModel, QAbstractListModel, QAbstractTableModel,
    QModelIndex, QPersistentModelIndex, Qt
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QLineEdit, QGridLayout, QDialog, QTableView, QComboBox, QPushButton
)

from best.view.utils import QVLine

from ..model.species import Species
from ..model.fullmodel import Ecosystem

class _PushPopModel(QAbstractItemModel):
    species: list[Species]

    def rowCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.species)

    def pop(self, row: int) -> Species:
        self.beginRemoveRows(QModelIndex(), row, row)
        species = self.species.pop(row)
        self.endRemoveRows()
        return species

    def push(self, species: Species) -> None:
        row = len(self.species)
        self.beginInsertRows(QModelIndex(), row, row)
        self.species.append(species)
        self.endInsertRows()

@dataclass
class SpeciesModel(QAbstractListModel, _PushPopModel):
    species: list[Species] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__init__()

    def data(self, index: Union[QModelIndex, QPersistentModelIndex],
             role: int) -> Union[str, Species, None]:
        if role == Qt.ItemDataRole.DisplayRole:
            species = self.species[index.row()]
            return species.name
        if role == Qt.ItemDataRole.UserRole:
            return self.species[index.row()]
        return None

@dataclass
class PopulationModel(QAbstractTableModel, _PushPopModel):
    species: list[Species] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__init__()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> str:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ['Species', 'Current Population (1000s)'][section]
        return super().headerData(section, orientation, role)

    def data(self, index: Union[QModelIndex, QPersistentModelIndex],
             role: int) -> Union[str, Species, None]:
        if role == Qt.ItemDataRole.DisplayRole:
            species = self.species[index.row()]
            if index.column() == 0:
                return species.name
            elif index.column() == 1:
                return str(species.population)
            else:
                raise RuntimeError('Unreachable')
        if role == Qt.ItemDataRole.UserRole:
            return self.species[index.row()]
        return None

    def setData(self, index: Union[QModelIndex, QPersistentModelIndex], value, role: int = ...) -> bool:
        if index.column() != 1:
            return False
        try:
            self.species[index.row()].population = float(value)
        except ValueError:
            return False
        else:
            return True

    def columnCount(self, parent: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        return 2

    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlags:
        if index.column() == 1:
            return super().flags(index) | Qt.ItemFlag.ItemIsEditable
        return super().flags(index)

class SpeciesDisplay(QDialog):
    def __init__(self, ecosystem: Ecosystem) -> None:
        super().__init__()
        self.setWindowTitle('Current Species Populations')
        self.resize(600, 400)

        self.populationModel = PopulationModel()
        self.speciesModel = SpeciesModel(ecosystem.allSpecies[:])

        self.populationView = QTableView(self)
        self.populationView.setModel(self.populationModel)
        self.populationView.resizeColumnsToContents()


        self.speciesSelect = QComboBox(self)
        self.speciesSelect.setPlaceholderText('Select Species')
        self.speciesSelect.setModel(self.speciesModel)

        self.populationInput = QLineEdit(self)
        self.populationInput.setPlaceholderText('Current Population Estimate (1000s)')
        validator = QDoubleValidator()
        validator.setBottom(0.0)
        self.populationInput.setValidator(validator)
        self.populationInput.textEdited.connect(self.checkPopulation) # type: ignore

        self.addButton = QPushButton('Add')
        self.addButton.clicked.connect(self.addSpecies) # type: ignore
        self.addButton.setEnabled(False) # since population is initially empty
        self.acceptButton = QPushButton('OK')
        self.acceptButton.clicked.connect(self.accept) # type: ignore
        self.acceptButton.setEnabled(False)

        layout = QGridLayout(self)
        layout.addWidget(self.populationView, 0, 0, 1, 5)
        layout.addWidget(self.speciesSelect, 1, 0)
        layout.addWidget(self.populationInput, 1, 1)
        layout.addWidget(self.addButton, 1, 2)
        layout.addWidget(QVLine(), 1, 3)
        layout.addWidget(self.acceptButton, 1, 4)

        self.setLayout(layout)

    def checkPopulation(self, text: str) -> None:
        try:
            float(text)
        except ValueError:
            self.addButton.setEnabled(False)
        else:
            self.addButton.setEnabled(True)

    def addSpecies(self) -> None:
        choice: int = self.speciesSelect.currentIndex()
        chosenSpecies = self.speciesModel.pop(choice)
        chosenSpecies.population = float(self.populationInput.text())
        self.populationModel.push(chosenSpecies)
        self.populationView.resizeColumnsToContents()
        if not self.speciesModel.species:
            self.acceptButton.setEnabled(True)
            self.speciesSelect.setEnabled(False)
            self.addButton.setEnabled(False)
