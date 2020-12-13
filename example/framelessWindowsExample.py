import os
import sys

from qtpy.QtCore import Qt, qInstallMessageHandler, QPoint
from qtpy.QtWidgets import QApplication

import qrainbowstyle
from qrainbowstyle.extras import OutputLogger, qt_message_handler
from qrainbowstyle.windows import (FramelessMainWindow, FramelessDialog, FramelessQuestionMessageBox,
                                   FramelessCriticalMessageBox, FramelessWarningMessageBox,
                                   FramelessInformationMessageBox, FramelessMessageBox)


def main():
    logmodule = qrainbowstyle.extras.OutputLogger()
    qInstallMessageHandler(qt_message_handler)

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet())
    qrainbowstyle.set_app_name("Frameless windows test")
    qrainbowstyle.set_app_icon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "github_logo.png"))

    mainwindow = FramelessMainWindow()
    mainwindow.show()

    dialog = FramelessDialog()
    dialog.show()

    text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vitae efficitur arcu, sed accumsan sem. 
    Interdum et malesuada fames ac ante ipsum primis in faucibus. Nulla sit amet rhoncus eros. Curabitur auctor, 
    mauris a tincidunt congue, libero libero porttitor urna, sed semper ligula libero nec leo. Phasellus feugiat 
    maximus auctor."""

    x = 0
    q = FramelessQuestionMessageBox()
    q.setText(text)
    q.show()
    q.move(QPoint(0, x*q.height()))

    x += 1
    c = FramelessCriticalMessageBox()
    c.setText(text)
    c.show()
    c.move(QPoint(0, x * c.height()))

    x += 1
    i = FramelessInformationMessageBox()
    i.setText(text)
    i.show()
    i.move(QPoint(0, x * i.height()))

    x += 1
    n = FramelessMessageBox()
    n.setText(text)
    n.show()
    n.move(QPoint(0, x * n.height()))

    x += 1
    w = FramelessWarningMessageBox()
    w.setText(text)
    w.show()
    w.move(QPoint(0, x * w.height()))

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
