from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel
from qtpy.QtCore import Qt, qInstallMessageHandler

import sys

import qrainbowstyle
from qrainbowstyle.widgets import StylePickerGrid, StylePickerHorizontal, StylePickerVertical
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

    groupbox = QGroupBox(win)
    groupbox_layout = QGridLayout(groupbox)
    groupbox.setLayout(groupbox_layout)

    groupbox_layout.addWidget(QLabel("StylePickerGrid:"), *(1, 1))
    groupbox_layout.addWidget(StylePickerGrid(2, groupbox), *(1, 2))

    groupbox_layout.addWidget(QLabel("StylePickerVertical:"), *(2, 1))
    groupbox_layout.addWidget(StylePickerVertical(groupbox), *(2, 2))

    groupbox_layout.addWidget(QLabel("StylePickerHorizontal:"), *(3, 1))
    groupbox_layout.addWidget(StylePickerHorizontal(groupbox), *(3, 2))

    win.addContentWidget(groupbox)
    win.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
