#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""QRainbowStyle default palette."""

# Standard library imports
from collections import OrderedDict

# package imports
from qrainbowstyle.colorsystem import *


class BasePalette:
    """Base class for palettes."""

    # Color
    COLOR_BACKGROUND_1 = ''
    COLOR_BACKGROUND_2 = ''
    COLOR_BACKGROUND_3 = ''
    COLOR_BACKGROUND_4 = ''
    COLOR_BACKGROUND_5 = ''
    COLOR_BACKGROUND_6 = ''

    COLOR_TEXT_1 = ''
    COLOR_TEXT_2 = ''
    COLOR_TEXT_3 = ''
    COLOR_TEXT_4 = ''

    COLOR_ACCENT_1 = ''
    COLOR_ACCENT_2 = ''
    COLOR_ACCENT_3 = ''
    COLOR_ACCENT_4 = ''
    COLOR_ACCENT_5 = ''

    OPACITY_TOOLTIP = 0

    # Size
    SIZE_BORDER_RADIUS = '4px'

    # Borders
    BORDER_1 = '1px solid $COLOR_BACKGROUND_1'
    BORDER_2 = '1px solid $COLOR_BACKGROUND_4'
    BORDER_3 = '1px solid $COLOR_BACKGROUND_6'

    BORDER_SELECTION_3 = '1px solid $COLOR_ACCENT_3'
    BORDER_SELECTION_2 = '1px solid $COLOR_ACCENT_2'
    BORDER_SELECTION_1 = '1px solid $COLOR_ACCENT_1'

    TITLE_BAR_BACKGROUND_COLOR = COLOR_ACCENT_3
    TITLE_BAR_BUTTONS_HOVER_COLOR = COLOR_ACCENT_4
    TITLE_BAR_BUTTONS_DISABLED_COLOR = COLOR_ACCENT_1
    TITLE_BAR_TEXT_COLOR = COLOR_TEXT_1

    # Paths
    PATH_RESOURCES = "':/qss_icons'"

    @classmethod
    def to_dict(cls, colors_only=False):
        """Convert variables to dictionary."""
        order = [
            'COLOR_BACKGROUND_6',
            'COLOR_BACKGROUND_5',
            'COLOR_BACKGROUND_4',
            'COLOR_BACKGROUND_2',
            'COLOR_BACKGROUND_3',
            'COLOR_BACKGROUND_1',
            'COLOR_TEXT_1',
            'COLOR_TEXT_2',
            'COLOR_TEXT_3',
            'COLOR_TEXT_4',
            'COLOR_ACCENT_1',
            'COLOR_ACCENT_2',
            'COLOR_ACCENT_3',
            'COLOR_ACCENT_4',
            'OPACITY_TOOLTIP',
            'SIZE_BORDER_RADIUS',
            'BORDER_1',
            'BORDER_2',
            'BORDER_3',
            'BORDER_SELECTION_3',
            'BORDER_SELECTION_2',
            'BORDER_SELECTION_1',
            'TITLE_BAR_BACKGROUND_COLOR',
            'TITLE_BAR_BUTTONS_HOVER_COLOR',
            'TITLE_BAR_BUTTONS_DISABLED_COLOR',
            'TITLE_BAR_TEXT_COLOR',
            'PATH_RESOURCES',
        ]
        dic = OrderedDict()
        for var in order:
            value = getattr(cls, var)

            if colors_only:
                if not var.startswith('COLOR'):
                    value = None

            if value:
                dic[var] = value

        return dic

    @classmethod
    def color_palette(cls):
        """Return the ordered colored palette dictionary."""
        return cls.to_dict(colors_only=True)


class Oceanic(BasePalette):
    """Theme variables."""
    COLOR_BACKGROUND_1 = "#263238"
    COLOR_BACKGROUND_2 = "#2f4048"
    COLOR_BACKGROUND_3 = "#34474f"
    COLOR_BACKGROUND_4 = "#394d57"
    COLOR_BACKGROUND_5 = "#3d545f"
    COLOR_BACKGROUND_6 = "#425b67"

    COLOR_TEXT_1 = Gray.B130
    COLOR_TEXT_2 = Gray.B110
    COLOR_TEXT_3 = Gray.B90
    COLOR_TEXT_4 = Gray.B80

    COLOR_ACCENT_1 = "#0a4542"
    COLOR_ACCENT_2 = "#136460"
    COLOR_ACCENT_3 = "#097D74"
    COLOR_ACCENT_4 = "#56BFBA"
    COLOR_ACCENT_5 = "#C4D6DB"

    TITLE_BAR_BACKGROUND_COLOR = COLOR_ACCENT_3
    TITLE_BAR_BUTTONS_HOVER_COLOR = COLOR_ACCENT_4
    TITLE_BAR_BUTTONS_DISABLED_COLOR = COLOR_ACCENT_1
    TITLE_BAR_TEXT_COLOR = COLOR_TEXT_1

    OPACITY_TOOLTIP = 230


class QDarkStyle(BasePalette):
    COLOR_BACKGROUND_1 = "#19232d"
    COLOR_BACKGROUND_2 = "#27323c"
    COLOR_BACKGROUND_3 = "#35414b"
    COLOR_BACKGROUND_4 = "#3e4b55"
    COLOR_BACKGROUND_5 = "#47555f"
    COLOR_BACKGROUND_6 = "#505f69"

    COLOR_TEXT_1 = Gray.B130
    COLOR_TEXT_2 = Gray.B110
    COLOR_TEXT_3 = Gray.B90
    COLOR_TEXT_4 = Gray.B80

    COLOR_ACCENT_1 = "#14506e"
    COLOR_ACCENT_2 = "#145f87"
    COLOR_ACCENT_3 = "#146998"
    COLOR_ACCENT_4 = "#1478b1"
    COLOR_ACCENT_5 = "#148cd2"

    TITLE_BAR_BACKGROUND_COLOR = COLOR_ACCENT_3
    TITLE_BAR_BUTTONS_HOVER_COLOR = COLOR_ACCENT_4
    TITLE_BAR_BUTTONS_DISABLED_COLOR = COLOR_ACCENT_1
    TITLE_BAR_TEXT_COLOR = COLOR_TEXT_1

    OPACITY_TOOLTIP = 230


class DarkOrange(BasePalette):
    COLOR_BACKGROUND_1 = Gray.B10
    COLOR_BACKGROUND_2 = Gray.B20
    COLOR_BACKGROUND_3 = Gray.B30
    COLOR_BACKGROUND_4 = Gray.B40
    COLOR_BACKGROUND_5 = Gray.B50
    COLOR_BACKGROUND_6 = Gray.B60

    COLOR_TEXT_1 = Gray.B130
    COLOR_TEXT_2 = Gray.B110
    COLOR_TEXT_3 = Gray.B90
    COLOR_TEXT_4 = Gray.B80

    COLOR_ACCENT_1 = "#ce4b01"
    COLOR_ACCENT_2 = "#d66522"
    COLOR_ACCENT_3 = "#de8044"
    COLOR_ACCENT_4 = "#e79b65"
    COLOR_ACCENT_5 = "#efb587"

    TITLE_BAR_BACKGROUND_COLOR = COLOR_ACCENT_3
    TITLE_BAR_BUTTONS_HOVER_COLOR = COLOR_ACCENT_4
    TITLE_BAR_BUTTONS_DISABLED_COLOR = COLOR_ACCENT_1
    TITLE_BAR_TEXT_COLOR = COLOR_TEXT_1

    OPACITY_TOOLTIP = 230


class LightOrange(BasePalette):
    COLOR_BACKGROUND_1 = Gray.B140
    COLOR_BACKGROUND_2 = Gray.B130
    COLOR_BACKGROUND_3 = Gray.B120
    COLOR_BACKGROUND_4 = Gray.B110
    COLOR_BACKGROUND_5 = Gray.B100
    COLOR_BACKGROUND_6 = Gray.B90

    COLOR_TEXT_1 = Gray.B10
    COLOR_TEXT_2 = Gray.B20
    COLOR_TEXT_3 = Gray.B50
    COLOR_TEXT_4 = Gray.B70

    COLOR_ACCENT_1 = "#ce4b01"
    COLOR_ACCENT_2 = "#d66522"
    COLOR_ACCENT_3 = "#de8044"
    COLOR_ACCENT_4 = "#e79b65"
    COLOR_ACCENT_5 = "#efb587"

    TITLE_BAR_BACKGROUND_COLOR = COLOR_ACCENT_3
    TITLE_BAR_BUTTONS_HOVER_COLOR = COLOR_ACCENT_4
    TITLE_BAR_BUTTONS_DISABLED_COLOR = COLOR_ACCENT_1
    TITLE_BAR_TEXT_COLOR = COLOR_TEXT_1

    OPACITY_TOOLTIP = 230


class QDarkStyle3Light(BasePalette):
    # Color
    COLOR_BACKGROUND_1 = Gray.B140
    COLOR_BACKGROUND_2 = Gray.B130
    COLOR_BACKGROUND_3 = Gray.B120
    COLOR_BACKGROUND_4 = Gray.B110
    COLOR_BACKGROUND_5 = Gray.B100
    COLOR_BACKGROUND_6 = Gray.B90

    COLOR_TEXT_1 = Gray.B10
    COLOR_TEXT_2 = Gray.B20
    COLOR_TEXT_3 = Gray.B50
    COLOR_TEXT_4 = Gray.B70

    COLOR_ACCENT_1 = Blue.B130
    COLOR_ACCENT_2 = Blue.B100
    COLOR_ACCENT_3 = Blue.B90
    COLOR_ACCENT_4 = Blue.B80
    COLOR_ACCENT_5 = Blue.B70

    TITLE_BAR_BACKGROUND_COLOR = COLOR_ACCENT_3
    TITLE_BAR_BUTTONS_HOVER_COLOR = COLOR_ACCENT_4
    TITLE_BAR_BUTTONS_DISABLED_COLOR = COLOR_ACCENT_1
    TITLE_BAR_TEXT_COLOR = COLOR_TEXT_1

    OPACITY_TOOLTIP = 230


class QDarkStyle3(BasePalette):
    # Color
    COLOR_BACKGROUND_1 = Gray.B10
    COLOR_BACKGROUND_2 = Gray.B20
    COLOR_BACKGROUND_3 = Gray.B30
    COLOR_BACKGROUND_4 = Gray.B40
    COLOR_BACKGROUND_5 = Gray.B50
    COLOR_BACKGROUND_6 = Gray.B60

    COLOR_TEXT_1 = Gray.B130
    COLOR_TEXT_2 = Gray.B110
    COLOR_TEXT_3 = Gray.B90
    COLOR_TEXT_4 = Gray.B80

    COLOR_ACCENT_1 = Blue.B20
    COLOR_ACCENT_2 = Blue.B40
    COLOR_ACCENT_3 = Blue.B50
    COLOR_ACCENT_4 = Blue.B70
    COLOR_ACCENT_5 = Blue.B80

    TITLE_BAR_BACKGROUND_COLOR = COLOR_ACCENT_3
    TITLE_BAR_BUTTONS_HOVER_COLOR = COLOR_ACCENT_4
    TITLE_BAR_BUTTONS_DISABLED_COLOR = COLOR_ACCENT_1
    TITLE_BAR_TEXT_COLOR = COLOR_TEXT_1

    OPACITY_TOOLTIP = 230
