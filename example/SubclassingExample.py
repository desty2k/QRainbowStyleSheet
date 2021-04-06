from qtpy.QtWidgets import QPushButton, QApplication, QMessageBox, QDialogButtonBox
from qtpy.QtCore import Slot, QMetaObject, Qt, qInstallMessageHandler
from qtpy.QtGui import QWindow

import sys

import qrainbowstyle
from qrainbowstyle.extras import OutputLogger, qt_message_handler
from qrainbowstyle.windows import FramelessWindow, FramelessQuestionMessageBox, FramelessWarningMessageBox


class BaseWindow(FramelessWindow):
    """Window subclassing frameless window."""

    def __init__(self):
        super(BaseWindow, self).__init__(None)
        self.win = None
        self.warning = None
        self.askClose = None

        self.subwindowButton = QPushButton("Create new subwindow", self)
        self.subwindowButton.setObjectName("subwindowButton")

        self.warningButton = QPushButton("Create new warning message box", self)
        self.warningButton.setObjectName("warningButton")

        self.idButton = QPushButton("Print ID", self)
        self.idButton.setObjectName("idButton")

        self.closeButton = QPushButton("Close application", self)
        self.closeButton.setObjectName("closeButton")

        self.addContentWidget(self.subwindowButton)
        self.addContentWidget(self.warningButton)
        self.addContentWidget(self.idButton)
        self.addContentWidget(self.closeButton)

        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_idButton_clicked(self):
        print(self.winId())

    @Slot()
    def on_subwindowButton_clicked(self):
        self.win = FramelessWindow(self)
        self.win.show()

    @Slot()
    def on_closeButton_clicked(self):
        self.askClose = FramelessQuestionMessageBox(self)
        self.askClose.setWindowModality(Qt.WindowModal)
        self.askClose.setText("Do you really want to exit?")
        self.askClose.setStandardButtons(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.askClose.button(QDialogButtonBox.No).clicked.connect(self.askClose.close)
        self.askClose.button(QDialogButtonBox.Yes).clicked.connect(self.close)
        self.askClose.show()

    @Slot()
    def on_warningButton_clicked(self):
        self.warning = FramelessWarningMessageBox(self)
        self.warning.setText("Frameless warning message box test text!")
        self.warning.show()


if __name__ == '__main__':
    logger = OutputLogger()
    qInstallMessageHandler(qt_message_handler)

    qrainbowstyle.useDarwinButtons()
    qrainbowstyle.alignButtonsLeft()
    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet("qdarkstyle3"))

    window = BaseWindow()
    window.show()

    sys.exit(app.exec_())
