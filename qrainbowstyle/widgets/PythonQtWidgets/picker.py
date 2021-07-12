from qtpy.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QApplication
from qtpy.QtCore import Signal, QSize
from qtpy.QtGui import QPixmap, QPainter, QPen, QColor, QIcon

import qrainbowstyle
from qrainbowstyle.utils import setStylesheetOnQApp


class Painter(QWidget):
    """Painter documentation"""

    def __init__(self, parent=None):
        super(Painter, self).__init__(parent)
        self.pixmap = None
        self.c1 = None
        self.c2 = None
        self.size = None

    def paintPixmap(self, size, c1, c2):
        self.size = size
        self.c1 = c1
        self.c2 = c2
        self.pixmap = QPixmap(size, size)

        self.paintEvent(None)
        return self.pixmap

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self.pixmap)
        painter.drawPixmap(0, 0, self.pixmap)

        pen1 = QPen(QColor(self.c1), 1)
        pen2 = QPen(QColor(self.c2), 2)

        painter.setPen(pen1)
        y = self.size - 1
        for x in range(self.size):
            painter.drawLine(0, x, y, x)
            y = y - 1

        painter.setPen(pen2)
        y = 1
        for x in range(self.size, 0, -1):
            painter.drawLine(y, x, self.size, x)
            y = y + 1

        painter.end()


class _PaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        side = 128
        self.setFixedSize(QSize(side, side))
        self.color = color

        self.setIcon(QIcon(Painter().paintPixmap(side, self.color[1], self.color[2])))
        stylesheet = """
        min-width: 24px;
        max-width: 24px;
        min-height: 24px;
        max-height: 24px;
        padding: 0px;
        border: none;
        """
        self.setIconSize(QSize(24, 24))
        self.setStyleSheet(stylesheet)


class _PaletteBase(QWidget):
    selected = Signal(object)

    def _emit_color(self, color):
        self.selected.emit(color)


class _PaletteLinearBase(_PaletteBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        colors = []

        for style in qrainbowstyle.getAvailablePalettes():
            colors.append({1: style.COLOR_BACKGROUND_1, 2: style.COLOR_ACCENT_3, "name": style.__name__})

        palette = self.layoutvh()

        for c in colors:
            b = _PaletteButton(c)
            b.pressed.connect(lambda color=c: setStylesheetOnQApp(style=color["name"]))
            palette.addWidget(b)

        self.setLayout(palette)


class StylePickerHorizontal(_PaletteLinearBase):
    layoutvh = QHBoxLayout


class StylePickerVertical(_PaletteLinearBase):
    layoutvh = QVBoxLayout


class StylePickerGrid(QWidget):
    """Select application color palette from a grid."""

    def __init__(self, n_columns=5, parent=None):
        super(StylePickerGrid, self).__init__(parent)
        self.setMaximumWidth(150)
        colors = []

        for style in qrainbowstyle.getAvailablePalettes():
            colors.append({1: style.COLOR_BACKGROUND_1, 2: style.COLOR_ACCENT_3, "name": style.__name__})

        palette = QGridLayout()
        row, col = 0, 0

        for c in colors:
            b = _PaletteButton(c)
            b.pressed.connect(lambda color=c: setStylesheetOnQApp(style=color["name"]))
            palette.addWidget(b, row, col)
            col += 1
            if col == n_columns:
                col = 0
                row += 1

        self.setLayout(palette)
