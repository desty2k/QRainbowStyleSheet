"""
The MIT License (MIT)

Copyright (c) 2017 fbjorn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QGridLayout, QGroupBox, QHBoxLayout, QSpinBox, QDoubleSpinBox, QPushButton, QLabel, QColorDialog, QApplication, QMessageBox

from pyqtspinner import WaitingSpinner

import qrainbowstyle
import qrainbowstyle.widgets
import qrainbowstyle.windows


class Demo(QWidget):
    sb_roundness = None
    sb_opacity = None
    sb_fadeperc = None
    sb_lines = None
    sb_line_length = None
    sb_line_width = None
    sb_inner_radius = None
    sb_rev_s = None

    btn_start = None
    btn_stop = None
    btn_pick_color = None

    spinner = None

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        groupbox1 = QGroupBox()
        groupbox1_layout = QHBoxLayout()
        groupbox2 = QGroupBox()
        groupbox2_layout = QGridLayout()
        button_hbox = QHBoxLayout()
        self.setLayout(grid)
        self.setWindowTitle("QtWaitingSpinner Creator")
        self.setWindowFlags(Qt.Dialog)

        # SPINNER
        self.spinner = WaitingSpinner(self)

        # Spinboxes
        self.sb_roundness = QDoubleSpinBox()
        self.sb_opacity = QDoubleSpinBox()
        self.sb_fadeperc = QDoubleSpinBox()
        self.sb_lines = QSpinBox()
        self.sb_line_length = QDoubleSpinBox()
        self.sb_line_width = QDoubleSpinBox()
        self.sb_inner_radius = QDoubleSpinBox()
        self.sb_rev_s = QDoubleSpinBox()

        # set spinbox default values
        self.sb_roundness.setValue(70)
        self.sb_roundness.setRange(0, 9999)
        self.sb_opacity.setValue(15)
        self.sb_opacity.setRange(0, 9999)
        self.sb_fadeperc.setValue(70)
        self.sb_fadeperc.setRange(0, 9999)
        self.sb_lines.setValue(12)
        self.sb_lines.setRange(1, 9999)
        self.sb_line_length.setValue(10)
        self.sb_line_length.setRange(0, 9999)
        self.sb_line_width.setValue(5)
        self.sb_line_width.setRange(0, 9999)
        self.sb_inner_radius.setValue(10)
        self.sb_inner_radius.setRange(0, 9999)
        self.sb_rev_s.setValue(1)
        self.sb_rev_s.setRange(0.1, 9999)

        # Buttons
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_pick_color = QPushButton("Pick Color")
        self.btn_show_init = QPushButton("Show init args")
        self.btn_fade_in = QPushButton("Fade in")
        self.btn_fade_out = QPushButton("Fade out")

        # Connects
        self.sb_roundness.valueChanged.connect(self.set_roundness)
        self.sb_opacity.valueChanged.connect(self.set_opacity)
        self.sb_fadeperc.valueChanged.connect(self.set_fadeperc)
        self.sb_lines.valueChanged.connect(self.set_lines)
        self.sb_line_length.valueChanged.connect(self.set_line_length)
        self.sb_line_width.valueChanged.connect(self.set_line_width)
        self.sb_inner_radius.valueChanged.connect(self.set_inner_radius)
        self.sb_rev_s.valueChanged.connect(self.set_rev_s)

        # qrainbowstyle
        self.picker = qrainbowstyle.widgets.StylePickerGrid(self)

        self.btn_start.clicked.connect(self.spinner_start)
        self.btn_stop.clicked.connect(self.spinner_stop)
        self.btn_pick_color.clicked.connect(self.show_color_picker)
        self.btn_show_init.clicked.connect(self.show_init_args)
        self.btn_fade_in.clicked.connect(self.fadeIn)
        self.btn_fade_out.clicked.connect(self.fadeOut)

        # Layout adds
        groupbox1_layout.addWidget(self.spinner)
        groupbox1.setLayout(groupbox1_layout)

        groupbox2_layout.addWidget(QLabel("Roundness:"), *(1, 1))
        groupbox2_layout.addWidget(self.sb_roundness, *(1, 2))
        groupbox2_layout.addWidget(QLabel("Opacity:"), *(2, 1))
        groupbox2_layout.addWidget(self.sb_opacity, *(2, 2))
        groupbox2_layout.addWidget(QLabel("Fade Perc:"), *(3, 1))
        groupbox2_layout.addWidget(self.sb_fadeperc, *(3, 2))
        groupbox2_layout.addWidget(QLabel("Lines:"), *(4, 1))
        groupbox2_layout.addWidget(self.sb_lines, *(4, 2))
        groupbox2_layout.addWidget(QLabel("Line Length:"), *(5, 1))
        groupbox2_layout.addWidget(self.sb_line_length, *(5, 2))
        groupbox2_layout.addWidget(QLabel("Line Width:"), *(6, 1))
        groupbox2_layout.addWidget(self.sb_line_width, *(6, 2))
        groupbox2_layout.addWidget(QLabel("Inner Radius:"), *(7, 1))
        groupbox2_layout.addWidget(self.sb_inner_radius, *(7, 2))
        groupbox2_layout.addWidget(QLabel("Rev/s:"), *(8, 1))
        groupbox2_layout.addWidget(self.sb_rev_s, *(8, 2))
        groupbox2_layout.addWidget(QLabel("Style: "), *(9, 1))
        groupbox2_layout.addWidget(self.picker, *(9, 2))

        groupbox2.setLayout(groupbox2_layout)

        button_hbox.addWidget(self.btn_start)
        button_hbox.addWidget(self.btn_stop)
        button_hbox.addWidget(self.btn_pick_color)
        button_hbox.addWidget(self.btn_show_init)
        button_hbox.addWidget(self.btn_fade_in)
        button_hbox.addWidget(self.btn_fade_out)

        grid.addWidget(groupbox1, *(1, 1))
        grid.addWidget(groupbox2, *(1, 2))
        grid.addLayout(button_hbox, *(2, 1))

        self.spinner.start()

    def set_roundness(self):
        self.spinner.setRoundness(self.sb_roundness.value())

    def set_opacity(self):
        self.spinner.setMinimumTrailOpacity(self.sb_opacity.value())

    def set_fadeperc(self):
        self.spinner.setTrailFadePercentage(self.sb_fadeperc.value())

    def set_lines(self):
        self.spinner.setNumberOfLines(self.sb_lines.value())

    def set_line_length(self):
        self.spinner.setLineLength(self.sb_line_length.value())

    def set_line_width(self):
        self.spinner.setLineWidth(self.sb_line_width.value())

    def set_inner_radius(self):
        self.spinner.setInnerRadius(self.sb_inner_radius.value())

    def set_rev_s(self):
        self.spinner.setRevolutionsPerSecond(self.sb_rev_s.value())

    def spinner_start(self):
        self.spinner.start()

    def spinner_stop(self):
        self.spinner.stop()

    def show_color_picker(self):
        self.spinner.setColor(QColorDialog.getColor())

    def show_init_args(self):
        text = (
            'WaitingSpinner(\n'
            '    parent,\n'
            '    roundness={}, opacity={},\n'
            '    fade={}, radius={}, lines={},\n'
            '    line_length={}, line_width={},\n'
            '    speed={}, color={}\n'
            ')\n'
        ).format(
            self.sb_roundness.value(), self.sb_opacity.value(),
            self.sb_fadeperc.value(), self.sb_inner_radius.value(),
            self.sb_lines.value(), self.sb_line_length.value(),
            self.sb_line_width.value(), self.sb_rev_s.value(),
            self.spinner.color.getRgb()[:3]
        )

        msg_box = QMessageBox(text=text)
        msg_box.setWindowTitle('Text was copied to clipboard')
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)
        print(text)
        msg_box.exec_()

    def fadeIn(self):
        self.spinner.fadeIn()

    def fadeOut(self):
        self.spinner.fadeOut()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet())
    win = qrainbowstyle.windows.FramelessWindow()
    main = Demo()
    win.addContentWidget(main)
    win.show()
    sys.exit(app.exec())
