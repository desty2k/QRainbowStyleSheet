from qtpy.QtWidgets import QApplication
from qtpy.QtCore import Qt, qInstallMessageHandler

import sys

import qrainbowstyle
from qrainbowstyle.widgets import StylePicker
from qrainbowstyle.windows import FramelessMainWindow
from qrainbowstyle.extras import OutputLogger, qt_message_handler


def main():
    logmodule = qrainbowstyle.extras.OutputLogger()
    qInstallMessageHandler(qt_message_handler)

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet())

    win = FramelessMainWindow()

    widget = StylePicker(win)

    win.addContentWidget(widget)
    win.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
