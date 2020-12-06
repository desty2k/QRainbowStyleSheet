from qtpy.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QApplication
from qtpy.QtCore import Signal, QSize
from qtpy.QtGui import QPixmap, QPainter, QPen, QColor, QIcon

import qrainbowstyle
from qrainbowstyle.utils import setStylesheetOnQApp


PALETTES = {
    # bokeh paired 12
    'paired12':['#000000', '#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928', '#ffffff'],
    # d3 category 10
    'category10':['#000000', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#ffffff'],
    # 17 undertones https://lospec.com/palette-list/17undertones
    '17undertones': ['#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49', '#458352','#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b', '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff']
}


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
    def __init__(self, colors, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(colors, str):
            if colors in PALETTES:
                colors = PALETTES[colors]

        palette = self.layoutvh()

        for c in colors:
            b = _PaletteButton(c)
            b.pressed.connect(
                lambda c=c: self._emit_color(c)
            )
            palette.addWidget(b)

        self.setLayout(palette)


class PaletteHorizontal(_PaletteLinearBase):
    layoutvh = QHBoxLayout


class PaletteVertical(_PaletteLinearBase):
    layoutvh = QVBoxLayout


class StylePicker(QWidget):
    """Select application color palette from a grid."""

    def __init__(self, parent):
        super(StylePicker, self).__init__(parent)
        self.setMaximumWidth(150)
        n_columns = 5
        colors = []
        if isinstance(colors, str):
            if colors in PALETTES:
                colors = PALETTES[colors]

        else:
            for style in qrainbowstyle.get_available_palettes():
                colors.append({1: style.COLOR_BACKGROUND_NORMAL, 2: style.COLOR_SELECTION_NORMAL, "name": style.__name__})

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
