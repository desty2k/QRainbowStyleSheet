from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QGridLayout, QLabel, QStyle, QDialogButtonBox, QSizePolicy)

from .framelessdialog import FramelessDialog


class FramelessMessageBox(FramelessDialog):
    """FramelessMessageBox documentation"""

    def __init__(self, parent=None):
        super(FramelessMessageBox, self).__init__(parent)
        self.resize(300, 100)

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setVerticalSpacing(8)
        self.grid.setHorizontalSpacing(0)

        self.iconLabel = QLabel(self)
        self.iconLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.iconLabel.setScaledContents(True)
        self.setIcon(QStyle.SP_MessageBoxInformation)
        self.grid.addWidget(self.iconLabel, 0, 0, 2, 1, Qt.AlignTop | Qt.AlignLeft)

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText("QMessageBox Dialog window text. Lorem ipsum mare guer sla ikure mier purso.")
        self.label.setContentsMargins(2, 0, 0, 0)
        self.label.setIndent(9)

        self.grid.addWidget(self.label, 0, 1, 1, 1)

        self.grid.setRowStretch(1, 100)
        self.grid.setRowMinimumHeight(2, 6)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.grid.addWidget(self.buttonBox, 3, 1, 1, 1)

        self.layout.addLayout(self.grid)
        self.showWindowIcon(False)

    def setText(self, text: str):
        self.label.setText(text)
