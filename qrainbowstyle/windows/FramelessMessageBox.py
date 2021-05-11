from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QGridLayout, QLabel, QStyle, QDialogButtonBox, QSizePolicy, QWidget, QApplication
from qtpy.QtGui import QIcon

from . import FramelessWindow


class FramelessMessageBox(FramelessWindow):
    """Frameless messagebox."""

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
        """Set standard buttons for message box.

        Args:
            buttons (StandardButtons): Standard buttons.
        """
        self.__buttonBox.setStandardButtons(buttons)

    def addButton(self, button, role):
        """Adds the given button to the button box with the specified role.
        If the role is invalid, the button is not added.

        If the button has already been added, it is removed and added again with the new role.

        Note: The button box takes ownership of the button.

        Args:
            button (StandardButton): Standard button.
            role (ButtonRole): Button role
        """
        self.__buttonBox.addButton(button, role)

    def removeButton(self, button):
        """Removes button from the button box without deleting it and sets its parent to zero.

        Args:
            button (StandardButton): Standard button.
        """
        self.__buttonBox.removeButton(button)

    def button(self, button):
        """Returns the QPushButton corresponding to the standard button which,
        or 0 if the standard button doesn't exist in this button box.

        Args:
            button (StandardButton): Standard button.
        """
        return self.__buttonBox.button(button)

    def buttons(self):
        """Returns a list of all the buttons that have been added to the button box."""
        return self.__buttonBox.buttons()

    def standardButtons(self):
        """This property holds collection of standard buttons in the button box.
        This property controls which standard buttons are used by the button box."""
        return self.__buttonBox.standardButtons()

    def standardButton(self, button):
        """Returns the standard button enum value corresponding to the given button,
        or NoButton if the given button isn't a standard button.

        Args:
            button (QAbstractButton): Standard button.
        """
        return self.__buttonBox.standardButton(button)

    def setText(self, text: str):
        """Set text for message box."""
        self.__textLabel.setText(text)
        self.__textLabel.adjustSize()
        self.__textLabel.updateGeometry()
        self.adjustSize()

    def text(self):
        """This property holds the message box text to be displayed.
        The default value of this property is an empty string."""
        return self.__textLabel.text()

    def setIcon(self, icon):
        """Set icon for message box.

        Args:
            icon (QIcon): Message box icon.
        """
        if icon:
            icon = QApplication.instance().style().standardIcon(icon)
            self.__iconLabel.setPixmap(icon.pixmap(QSize(128, 128)))
        else:
            self.__iconLabel.setPixmap(QIcon().pixmap(QSize(128, 128)))

    def icon(self):
        """This property holds the message box's icon"""
        return QIcon(self.__iconLabel.pixmap())


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
