#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""QRainbowStyle default palette."""

# Standard library imports
from collections import OrderedDict

# package imports
from qrainbowstyle.colorsystem import *


class BasePalette:
    """Base class for palettes."""

    # buttons background, active tabs name background, titlebar icons background on hover
    COLOR_BACKGROUND_LIGHT = '#505F69'
    # borders, non-active tabs names, headers in tables, titlebar icons background
    COLOR_BACKGROUND_NORMAL = '#32414B'
    # widgets background
    COLOR_BACKGROUND_DARK = '#19232D'

    # text
    COLOR_FOREGROUND_LIGHT = '#F0F0F0'
    # not used?
    COLOR_FOREGROUND_NORMAL = '#AAAAAA'
    # disabled widgets text
    COLOR_FOREGROUND_DARK = '#787878'

    # borders on selection
    COLOR_SELECTION_LIGHT = '#148CD2'
    # checked widgets borders, current tab indicator
    COLOR_SELECTION_NORMAL = '#1464A0'
    # disabled widgets borders, disabled tabs indicators
    COLOR_SELECTION_DARK = '#14506E'

    OPACITY_TOOLTIP = 230

    # Size
    SIZE_BORDER_RADIUS = '4px'

    # Borders
    BORDER_LIGHT = '1px solid $COLOR_BACKGROUND_LIGHT'
    BORDER_NORMAL = '1px solid $COLOR_BACKGROUND_NORMAL'
    BORDER_DARK = '1px solid $COLOR_BACKGROUND_DARK'

    BORDER_SELECTION_LIGHT = '1px solid $COLOR_SELECTION_LIGHT'
    BORDER_SELECTION_NORMAL = '1px solid $COLOR_SELECTION_NORMAL'
    BORDER_SELECTION_DARK = '1px solid $COLOR_SELECTION_DARK'

    # Example of additional widget specific variables
    W_STATUS_BAR_BACKGROUND_COLOR = COLOR_SELECTION_DARK

    # Paths
    PATH_RESOURCES = "':/qss_icons'"

    @classmethod
    def to_dict(cls, colors_only=False):
        """Convert variables to dictionary."""
        order = [
            'COLOR_BACKGROUND_LIGHT',
            'COLOR_BACKGROUND_NORMAL',
            'COLOR_BACKGROUND_DARK',
            'COLOR_FOREGROUND_LIGHT',
            'COLOR_FOREGROUND_NORMAL',
            'COLOR_FOREGROUND_DARK',
            'COLOR_SELECTION_LIGHT',
            'COLOR_SELECTION_NORMAL',
            'COLOR_SELECTION_DARK',
            'OPACITY_TOOLTIP',
            'SIZE_BORDER_RADIUS',
            'BORDER_LIGHT',
            'BORDER_NORMAL',
            'BORDER_DARK',
            'BORDER_SELECTION_LIGHT',
            'BORDER_SELECTION_NORMAL',
            'BORDER_SELECTION_DARK',
            'W_STATUS_BAR_BACKGROUND_COLOR',
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


class QDarkStyle(BasePalette):
    """Theme variables."""

    # Color
    COLOR_BACKGROUND_LIGHT = '#505F69'
    COLOR_BACKGROUND_NORMAL = '#32414B'
    COLOR_BACKGROUND_DARK = '#19232D'

    COLOR_FOREGROUND_LIGHT = '#F0F0F0'
    COLOR_FOREGROUND_NORMAL = '#AAAAAA'
    COLOR_FOREGROUND_DARK = '#787878'

    COLOR_SELECTION_LIGHT = '#148CD2'
    COLOR_SELECTION_NORMAL = '#1464A0'
    COLOR_SELECTION_DARK = '#14506E'

    W_STATUS_BAR_BACKGROUND_COLOR = COLOR_SELECTION_DARK


class Oceanic(BasePalette):
    """Theme variables."""

    # Color
    COLOR_BACKGROUND_LIGHT = '#314147'
    COLOR_BACKGROUND_NORMAL = '#3B4950'
    COLOR_BACKGROUND_DARK = '#263238'

    COLOR_FOREGROUND_LIGHT = '#C4D6DB'
    COLOR_FOREGROUND_NORMAL = '#56BFBA'
    COLOR_FOREGROUND_DARK = '#56BFBA'

    COLOR_SELECTION_LIGHT = '#097D74'
    COLOR_SELECTION_NORMAL = '#136460'
    COLOR_SELECTION_DARK = '#1B2529'

    W_STATUS_BAR_BACKGROUND_COLOR = COLOR_SELECTION_DARK


class Cyberpunk(BasePalette):
    """Theme variables."""

    # Color
    COLOR_BACKGROUND_LIGHT = '#314147'
    COLOR_BACKGROUND_NORMAL = '#010014'
    COLOR_BACKGROUND_DARK = '#090D0C'

    COLOR_FOREGROUND_LIGHT = '#FBEC08'
    COLOR_FOREGROUND_NORMAL = '#49666e'
    COLOR_FOREGROUND_DARK = '#EC1E77'

    COLOR_SELECTION_LIGHT = '#51BCE2'
    COLOR_SELECTION_NORMAL = '#51BCE2'
    COLOR_SELECTION_DARK = '#51BCE2'

    W_STATUS_BAR_BACKGROUND_COLOR = COLOR_SELECTION_DARK


class DarkOrange(BasePalette):
    COLOR_BACKGROUND_LIGHT = Gray.B50
    COLOR_BACKGROUND_NORMAL = Gray.B30
    COLOR_BACKGROUND_DARK = Gray.B10

    COLOR_FOREGROUND_LIGHT = Gray.B120
    COLOR_FOREGROUND_NORMAL = Gray.B80
    COLOR_FOREGROUND_DARK = Gray.B60

    COLOR_SELECTION_LIGHT = Orange.B80
    COLOR_SELECTION_NORMAL = Orange.B70
    COLOR_SELECTION_DARK = Orange.B60

    W_STATUS_BAR_BACKGROUND_COLOR = COLOR_SELECTION_DARK


class LightOrange(BasePalette):
    COLOR_BACKGROUND_LIGHT = Gray.B140
    COLOR_BACKGROUND_NORMAL = Gray.B110
    COLOR_BACKGROUND_DARK = Gray.B120

    COLOR_FOREGROUND_LIGHT = Gray.B10
    COLOR_FOREGROUND_NORMAL = Gray.B30
    COLOR_FOREGROUND_DARK = Gray.B50

    COLOR_SELECTION_LIGHT = Orange.B80
    COLOR_SELECTION_NORMAL = Orange.B70
    COLOR_SELECTION_DARK = Orange.B60

    W_STATUS_BAR_BACKGROUND_COLOR = COLOR_SELECTION_DARK


class QDarkStyle3(BasePalette):
    COLOR_BACKGROUND_LIGHT = Gray.B50
    COLOR_BACKGROUND_NORMAL = Gray.B30
    COLOR_BACKGROUND_DARK = Gray.B10

    COLOR_FOREGROUND_LIGHT = Gray.B120
    COLOR_FOREGROUND_NORMAL = Gray.B80
    COLOR_FOREGROUND_DARK = Gray.B60

    COLOR_SELECTION_LIGHT = Blue.B60
    COLOR_SELECTION_NORMAL = Blue.B40
    COLOR_SELECTION_DARK = Blue.B20

    W_STATUS_BAR_BACKGROUND_COLOR = COLOR_SELECTION_DARK
