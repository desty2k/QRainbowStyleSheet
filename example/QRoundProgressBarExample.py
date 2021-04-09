from qtpy.QtWidgets import QApplication, QWidget, QFormLayout, QSlider, QPushButton, QHBoxLayout, QLabel
from qtpy.QtCore import Qt, qInstallMessageHandler

import sys

import qrainbowstyle
from qrainbowstyle.widgets import QRoundProgressBar, StylePickerHorizontal
from qrainbowstyle.windows import FramelessWindow
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
        self._controlWidgetLayout = QFormLayout(self._controlWidget)
        self._controlWidget.setLayout(self._controlWidgetLayout)

        bar_style_label = QLabel("Bar style", self._controlWidget)
        style = QPushButton(self._controlWidget)
        style.setMaximumWidth(200)
        style.setText("Change bar style")
        self._controlWidgetLayout.addRow(bar_style_label, style)

        app_style_label = QLabel("App style", self._controlWidget)
        picker = StylePickerHorizontal(self._controlWidget)
        picker.setMaximumWidth(200)
        self._controlWidgetLayout.addRow(app_style_label, picker)

        style.clicked.connect(lambda: roundbar.setBarStyle(get_style()))

        slider_label = QLabel("Progress", self._controlWidget)
        slider = QSlider(Qt.Horizontal, self._controlWidget)
        slider.setRange(0, 100)
        slider.valueChanged.connect(roundbar.setValue)
        slider.setMaximumWidth(200)
        slider.setValue(28)
        self._controlWidgetLayout.addRow(slider_label, slider)
        self._layout.addWidget(self._controlWidget)


def main():
    logmodule = qrainbowstyle.extras.OutputLogger()
    qInstallMessageHandler(qt_message_handler)

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet(style="darkorange"))

    win = FramelessWindow()

    widget = MainWidget(win)
    win.addContentWidget(widget)
    win.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
