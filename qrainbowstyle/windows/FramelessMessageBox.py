from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QGridLayout, QLabel, QStyle, QDialogButtonBox, QSizePolicy, QWidget, QApplication
from qtpy.QtGui import QIcon

from . import FramelessWindow


class FramelessMessageBox(FramelessWindow):

    def __init__(self, icon=None, parent=None):
        super(FramelessMessageBox, self).__init__(parent)
        self.setResizingEnabled(False)
        self.resize(QSize(350, 150))
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

        self.__messagewidget = QWidget(self)
        self.__messagewidget.setContentsMargins(11, 11, 11, 11)

        self.__grid = QGridLayout(self.__messagewidget)
        self.__grid.setContentsMargins(0, 0, 0, 0)
        self.__grid.setVerticalSpacing(8)
        self.__grid.setHorizontalSpacing(0)

        self.__messagewidget.setLayout(self.__grid)

        self.__iconLabel = QLabel(self.__messagewidget)
        self.__iconLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.__iconLabel.setScaledContents(True)
        self.__grid.addWidget(self.__iconLabel, 0, 0, 2, 1, Qt.AlignTop | Qt.AlignLeft)

        self.__textLabel = QLabel(self.__messagewidget)
        self.__textLabel.setWordWrap(True)
        self.__textLabel.setContentsMargins(2, 0, 0, 0)
        self.__textLabel.setIndent(9)
        self.__textLabel.setScaledContents(True)
        self.__textLabel.setMouseTracking(True)
        self.__textLabel.autoFillBackground()
        self.__textLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.__grid.addWidget(self.__textLabel, 0, 1, 1, 1)

        self.__grid.setRowStretch(1, 100)
        self.__grid.setRowMinimumHeight(2, 6)

        self.__buttonBox = QDialogButtonBox(self.__messagewidget)
        self.__buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.__grid.addWidget(self.__buttonBox, 3, 1, 1, 1)

        self.addContentWidget(self.__messagewidget)
        self.setIcon(icon)

        self.showSizeControl(False)
        self.setEdgeSnapping(False)

    def setStandardButtons(self, buttons):
        self.__buttonBox.setStandardButtons(buttons)

    def addButton(self, button, role):
        self.__buttonBox.addButton(button, role)

    def removeButton(self, button):
        self.__buttonBox.removeButton(button)

    def button(self, button):
        return self.__buttonBox.button(button)

    def buttons(self):
        return self.__buttonBox.buttons()

    def standardButtons(self):
        return self.__buttonBox.standardButtons()

    def standardButton(self, button):
        return self.__buttonBox.standardButton(button)

    def setText(self, text: str):
        self.__textLabel.setText(text)
        self.__textLabel.adjustSize()
        self.__textLabel.updateGeometry()
        self.adjustSize()

    def text(self):
        return self.__textLabel.text()

    def setIcon(self, icon):
        if icon:
            icon = QApplication.instance().style().standardIcon(icon)
            self.__iconLabel.setPixmap(icon.pixmap(QSize(128, 128)))
        else:
            self.__iconLabel.setPixmap(QIcon().pixmap(QSize(128, 128)))


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
