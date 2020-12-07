from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QPushButton
from qtpy.QtCore import Qt, qInstallMessageHandler

import sys

import qrainbowstyle
from qrainbowstyle.widgets import QRoundProgressBar, StylePicker
from qrainbowstyle.windows import FramelessMainWindow
from qrainbowstyle.extras import OutputLogger, qt_message_handler

styles = [QRoundProgressBar.BarStyle.PIE, QRoundProgressBar.BarStyle.DONUT, QRoundProgressBar.BarStyle.EXPAND,
          QRoundProgressBar.BarStyle.LINE]
style_index = 0


def get_style():
    global style_index
    style_index = style_index + 1
    if style_index > len(styles) - 1:
        style_index = 0
    return styles[style_index]


def main():
    logmodule = qrainbowstyle.extras.OutputLogger()
    qInstallMessageHandler(qt_message_handler)

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet(style="darkorange"))

    win = FramelessMainWindow()

    widget = QWidget(win)
    layout = QVBoxLayout(widget)
    widget.setLayout(layout)

    style = QPushButton(win)
    style.setText("Change bar style")
    layout.addWidget(style)

    picker = StylePicker(win)
    layout.addWidget(picker)

    roundbar = QRoundProgressBar(widget)
    roundbar.setBarStyle(QRoundProgressBar.BarStyle.PIE)
    roundbar.setFixedWidth(300)
    roundbar.setFixedHeight(300)
    roundbar.setDecimals(1)
    layout.addWidget(roundbar)

    style.clicked.connect(lambda: roundbar.setBarStyle(get_style()))

    slider = QSlider(Qt.Horizontal, widget)
    slider.setRange(0, 100)
    layout.addWidget(slider)
    slider.valueChanged.connect(roundbar.setValue)
    slider.setValue(28)

    win.addContentWidget(widget)
    win.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
