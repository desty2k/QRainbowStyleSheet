from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QGridLayout, QLabel, QStyle, QDialogButtonBox, QSizePolicy, QWidget, QApplication
from qtpy.QtGui import QIcon

from .framelessdialog import FramelessDialog


class FramelessMessageBox(FramelessDialog):
    """FramelessMessageBox documentation"""

    def __init__(self, icon=None, parent=None):
        super(FramelessMessageBox, self).__init__(parent)
        self.setResizingEnabled(False)
        self.resize(350, 150)

        self._messagewidget = QWidget(self)
        self._messagewidget.setContentsMargins(11, 5, 11, 11)

        self._grid = QGridLayout(self._messagewidget)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setVerticalSpacing(8)
        self._grid.setHorizontalSpacing(0)

        self._messagewidget.setLayout(self._grid)

        self._iconLabel = QLabel(self._messagewidget)
        self._iconLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self._iconLabel.setScaledContents(True)
        self._grid.addWidget(self._iconLabel, 0, 0, 2, 1, Qt.AlignTop | Qt.AlignLeft)

        self._textLabel = QLabel(self._messagewidget)
        self._textLabel.setWordWrap(True)
        self._textLabel.setContentsMargins(2, 0, 0, 0)
        self._textLabel.setIndent(9)
        self._textLabel.setScaledContents(True)
        self._textLabel.setMouseTracking(True)
        self._textLabel.autoFillBackground()
        self._textLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self._grid.addWidget(self._textLabel, 0, 1, 1, 1)

        self._grid.setRowStretch(1, 100)
        self._grid.setRowMinimumHeight(2, 6)

        self.buttonBox = QDialogButtonBox(self._messagewidget)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self._grid.addWidget(self.buttonBox, 3, 1, 1, 1)

        self.addContentWidget(self._messagewidget)
        self.setIcon(icon)

    def setStandardButtons(self, buttons):
        self.buttonBox.setStandardButtons(buttons)

    def addButton(self, button, role):
        self.buttonBox.addButton(button, role)

    def removeButton(self, button):
        self.buttonBox.removeButton(button)

    def button(self, button):
        return self.buttonBox.button(button)

    def buttons(self):
        return self.buttonBox.buttons()

    def standardButtons(self):
        return self.buttonBox.standardButtons()

    def standardButton(self, button):
        return self.buttonBox.standardButton(button)

    def setText(self, text: str):
        self._textLabel.setText(text)
        self._textLabel.adjustSize()
        self._textLabel.updateGeometry()

        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        policy.setHeightForWidth(True)
        self._textLabel.setSizePolicy(policy)
        self.setSizePolicy(policy)
        self.adjustSize()

    def text(self):
        return self._textLabel.text()

    def setIcon(self, icon):
        if icon:
            icon = QApplication.style().standardIcon(icon)
            self._iconLabel.setPixmap(icon.pixmap(QSize(128, 128)))
        else:
            self._iconLabel.setPixmap(QIcon().pixmap(QSize(128, 128)))


class FramelessWarningMessageBox(FramelessMessageBox):
    def __init__(self, parent=None):
        super(FramelessWarningMessageBox, self).__init__(icon=QStyle.SP_MessageBoxWarning, parent=parent)


class FramelessInformationMessageBox(FramelessMessageBox):
    def __init__(self, parent=None):
        super(FramelessInformationMessageBox, self).__init__(icon=QStyle.SP_MessageBoxInformation, parent=parent)


class FramelessCriticalMessageBox(FramelessMessageBox):
    def __init__(self, parent=None):
        super(FramelessCriticalMessageBox, self).__init__(icon=QStyle.SP_MessageBoxCritical, parent=parent)


class FramelessQuestionMessageBox(FramelessMessageBox):
    def __init__(self, parent=None):
        super(FramelessQuestionMessageBox, self).__init__(icon=QStyle.SP_MessageBoxQuestion, parent=parent)
