from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QPushButton, QHBoxLayout, QLabel, QSizePolicy
from qtpy.QtCore import Qt, qInstallMessageHandler

import sys

import qrainbowstyle
from qrainbowstyle.widgets import QRoundProgressBar, StylePickerHorizontal
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


class MainWidget(QWidget):
    """MainWidget documentation"""

    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)

        self._layout = QHBoxLayout(self)
        self.setLayout(self._layout)

        roundbar = QRoundProgressBar(self)
        roundbar.setBarStyle(QRoundProgressBar.BarStyle.PIE)
        roundbar.setFixedWidth(300)
        roundbar.setFixedHeight(300)
        roundbar.setDecimals(1)
        self._layout.addWidget(roundbar)

        self._controlWidget = QWidget(self)
        self._controlWidget.setMaximumHeight(200)
        self._controlWidgetLayout = QVBoxLayout(self._controlWidget)
        self._controlWidget.setLayout(self._controlWidgetLayout)

        style = QPushButton(self._controlWidget)
        style.setText("Change bar style")
        self._controlWidgetLayout.addWidget(style)

        label = QLabel(self._controlWidget)
        label.setText("Change app style")
        self._controlWidgetLayout.addWidget(label)

        picker = StylePickerHorizontal(self._controlWidget)
        picker.setMaximumWidth(200)
        self._controlWidgetLayout.addWidget(picker)

        style.clicked.connect(lambda: roundbar.setBarStyle(get_style()))

        slider = QSlider(Qt.Horizontal, self._controlWidget)
        slider.setRange(0, 100)
        slider.valueChanged.connect(roundbar.setValue)
        slider.setValue(28)
        self._controlWidgetLayout.addWidget(slider)

        self._layout.addWidget(self._controlWidget)


def main():
    logmodule = qrainbowstyle.extras.OutputLogger()
    qInstallMessageHandler(qt_message_handler)

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet(style="darkorange"))

    win = FramelessMainWindow()

    widget = MainWidget(win)
    win.addContentWidget(widget)
    win.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
