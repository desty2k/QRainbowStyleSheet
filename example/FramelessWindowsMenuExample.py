import os
import sys

from qtpy.QtCore import Qt, qInstallMessageHandler
from qtpy.QtWidgets import QApplication, QMenu, QAction

import qrainbowstyle
from qrainbowstyle.extras import OutputLogger, qt_message_handler
from qrainbowstyle.utils import StyleLooper
from qrainbowstyle.windows import FramelessWindow, FramelessWarningMessageBox


def main():
    logmodule = qrainbowstyle.extras.OutputLogger()
    qInstallMessageHandler(qt_message_handler)

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet(style="oceanic"))
    qrainbowstyle.setAppName("Frameless dialog")
    qrainbowstyle.setAppIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "github_logo.png"))

    dialog = FramelessWindow()
    dialog.setWindowTitle("FDialog")
    dialog.resize(1100, 600)
    dialog.show()

    oneMenu = QMenu()
    oneMenu.setTitle("Tools")
    oneMenu.addActions([QAction("Clicker", oneMenu), QAction("Initializer", oneMenu)])

    twomenu = QMenu()
    twomenu.setTitle("File")
    twomenu.addActions([QAction("Open", twomenu), QAction("Save", twomenu)])

    thirdmenu = QMenu()
    thirdmenu.setTitle("Settings")
    thirdmenu.addActions([QAction("Network", thirdmenu)])

    looper = StyleLooper()
    style = QAction("Change style", thirdmenu)
    style.triggered.connect(looper.change)
    thirdmenu.addAction(style)

    dialog.addMenu(twomenu)
    dialog.addMenu(oneMenu)
    dialog.addMenu(thirdmenu)

    box = FramelessWarningMessageBox(dialog)
    box.setText("Warning :)")
    box.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
