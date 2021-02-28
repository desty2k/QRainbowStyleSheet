#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""QRainbowStyle is a fully customizable stylesheet for Python and Qt applications.

This module provides a function to load pre-compiled stylesheets. To generate your own
style based on custom color palette clone package from project homepage.

qrainbowstyle.windows module adds frameless windows, which can replace original QMainWindow,
QDialog and QMessageBox windows. Frameless windows support resizing, moving, snapping to edges.
You can set global icon and app name for all windows you create in your app. In frameless
main window it is also possible to set custom QMenu to QToolButton with app icon.

First, start importing our module

.. code-block:: python

    import qrainbowstyle

Then you can get stylesheet provided by QRainbowStyle for various Qt wrappers
as shown below

.. code-block:: python

    # PySide2
    stylesheet = qrainbowstyle.load_stylesheet_pyside2(style='darkblue')
    # PyQt5
    stylesheet = qrainbowstyle.load_stylesheet_pyqt5(style='darkblue')

Alternatively, from environment variables provided by QtPy, Qt.Py

.. code-block:: python

    # QtPy
    stylesheet =  qrainbowstyle.load_stylesheet(style='darkblue')
    # Qt.Py
    stylesheet = qrainbowstyle.load_stylesheet(style='darkblue', qt_api=Qt.__binding__)

Finally, set your QApplication with it

.. code-block:: python

    app.setStyleSheet(stylesheet)

To load frameless window in your app import both qrainbowstyle and qrainbowstyle.windows modules

.. code-block:: python

    import qrainbowstyle
    import qrainbowstyle.windows

Initialize qt app and load choosen stylesheet.
Next, create instances of frameless window and your master widget with content you want to show.

.. code-block:: python

    # Create app and load selected stylesheet
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet(style="cyberpunk"))

    # Package options
    # qrainbowstyle.align_buttons_left()      # align titlebar buttons to left side
    # qrainbowstyle.use_darwin_buttons()      # use darwin style buttons
    qrainbowstyle.set_app_name("My new application")  # set global name for application
    # qrainbowstyle.set_app_icon("icon.ico")    # set global app icon

    # Create frameless mainwindow
    win = qrainbowstyle.windows.FramelessMainWindow()

    # Create content widget and pass reference to main window
    widget = MasterWidget(win)

    # Add widget to main window and show it
    win.addContentWidget(widget)
    win.show()

    sys.exit(app.exec())

Enjoy!

"""

# Standard library imports
import os
import sys
import inspect
import logging
import platform
import qrainbowstyle

__version__ = "0.7.1"

_logger = logging.getLogger("qrainbowstyle")

# Folder's path
REPO_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

EXAMPLE_PATH = os.path.join(REPO_PATH, 'example')
IMAGES_PATH = os.path.join(REPO_PATH, 'images')
PACKAGE_PATH = os.path.join(REPO_PATH, 'qrainbowstyle')

QSS_PATH = os.path.join(PACKAGE_PATH, 'qss')
RC_PATH = os.path.join(PACKAGE_PATH, 'rc')
SVG_PATH = os.path.join(PACKAGE_PATH, 'svg')
STYLES_PATH = os.path.join(PACKAGE_PATH, 'styles')

BUTTONS_DARWIN_PATH = os.path.join(SVG_PATH, 'buttons_darwin')
BUTTONS_NT_PATH = os.path.join(SVG_PATH, 'buttons_nt')

# File names
QSS_FILE = 'style.qss'
QRC_FILE = QSS_FILE.replace('.qss', '.qrc')

MAIN_SCSS_FILE = 'main.scss'
STYLES_SCSS_FILE = '_styles.scss'
VARIABLES_SCSS_FILE = '_variables.scss'

# File paths
QSS_FILEPATH = os.path.join(PACKAGE_PATH, QSS_FILE)
QRC_FILEPATH = os.path.join(PACKAGE_PATH, QRC_FILE)

MAIN_SCSS_FILEPATH = os.path.join(QSS_PATH, MAIN_SCSS_FILE)
STYLES_SCSS_FILEPATH = os.path.join(QSS_PATH, STYLES_SCSS_FILE)
VARIABLES_SCSS_FILEPATH = os.path.join(QSS_PATH, VARIABLES_SCSS_FILE)

USE_DARWIN_BUTTONS = False
ALIGN_BUTTONS_LEFT = False

# Global app name
APP_NAME = None

# Path to app icon
APP_ICON_PATH = None


def set_app_name(name: str):
    """Set global app name which will be used in titlebars"""
    qrainbowstyle.APP_NAME = name


def set_app_icon(icon_path: str):
    """Set path to app icon which will be used in titlebars"""
    qrainbowstyle.APP_ICON_PATH = icon_path


def align_buttons_left():
    """Align titlebar buttons to left"""
    qrainbowstyle.ALIGN_BUTTONS_LEFT = True
    _logger.info("Buttons will be aligned to left")


def use_darwin_buttons():
    """Use darwin styled buttons everywhere in app"""
    qrainbowstyle.USE_DARWIN_BUTTONS = True
    _logger.info("Darwin buttons style has been enabled")


def get_available_styles():
    """Get list of available styles"""
    return [x for x in os.listdir(STYLES_PATH) if x not in ('__pycache__', '__init__.py')]


def get_available_palettes() -> list:
    """Get list of available palettes"""
    import qrainbowstyle.palette as source
    palettes = []
    for name, obj in inspect.getmembers(source):
        if inspect.isclass(obj) and issubclass(obj, source.BasePalette) and obj is not source.BasePalette:
            palettes.append(obj)
    return palettes


def get_current_palette():
    """Returns loaded palette"""
    try:
        from style_rc import palette  # noqa
        return palette
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Cannot find current palette. Did you load style sheet?")


def rainbowize(text: str) -> str:
    """Replaces colors names to hashes in text"""
    color_dict = get_current_palette().to_dict()
    for color in color_dict:
        text = text.replace(color, str(color_dict[color]))
    return text


def _apply_os_patches(palette):
    """
    Apply OS-only specific stylesheet pacthes.

    Returns:
        str: stylesheet string (css).
    """
    os_fix = ""

    if platform.system().lower() == 'darwin':
        # See issue #12
        os_fix = '''
        QDockWidget::title
        {{
            background-color: {color};
            text-align: center;
            height: 12px;
        }}
        '''.format(color=palette.COLOR_BACKGROUND_NORMAL)

    # Only open the QSS file if any patch is needed
    if os_fix:
        _logger.info("Found OS patches to be applied.")

    return os_fix


def _apply_binding_patches():
    """
    Apply binding-only specific stylesheet patches for the same OS.

    Returns:
        str: stylesheet string (css).
    """
    binding_fix = ""

    if binding_fix:
        _logger.info("Found binding patches to be applied.")

    return binding_fix


def _apply_version_patches():
    """
    Apply version-only specific stylesheet patches for the same binding.

    Returns:
        str: stylesheet string (css).
    """
    version_fix = ""

    if version_fix:
        _logger.info("Found version patches to be applied.")

    return version_fix


def _apply_application_patches(palette, QCoreApplication, QPalette, QColor):
    """
    Apply application level fixes on the QPalette.

    The import names args must be passed here because the import is done
    inside the load_stylesheet() function, as QtPy is only imported in
    that moment for setting reasons.
    """
    # See issue #139
    color = palette.COLOR_SELECTION_LIGHT
    qcolor = QColor(color)

    # Todo: check if it is qcoreapplication indeed
    app = QCoreApplication.instance()

    _logger.info("Found application patches to be applied.")

    if app:
        _palette = app.palette()
        _palette.setColor(QPalette.Normal, QPalette.Link, qcolor)
        app.setPalette(_palette)
    else:
        _logger.warning("No QCoreApplication instance found. "
                        "Application patches not applied. "
                        "You have to call load_stylesheet function after "
                        "instantiation of QApplication to take effect. ")


def _load_stylesheet(qt_api='', style=''):
    """
    Load the stylesheet based on QtPy abstraction layer environment variable.

    If the argument is not passed, it uses the current QT_API environment
    variable to make the imports of Qt bindings. If passed, it sets this
    variable then make the imports.

    Args:
        qt_api (str): qt binding name to set QT_API environment variable.
                      Default is ''. Possible values are pyside2,
                      pyqt5. Not case sensitive.

    Note:
        - Note that the variable QT_API is read when first imported. So,
          pay attention to the import order.
        - OS, binding and binding version number, and application specific
          patches are applied in this order.

    Returns:
        str: stylesheet string (css).
    """

    if qt_api:
        os.environ['QT_API'] = qt_api

    # Import is made after setting QT_API
    from qtpy.QtCore import QCoreApplication, QFile, QTextStream
    from qtpy.QtGui import QColor, QPalette

    # Search for style in styles directory
    style_dir = None

    available_styles = [x for x in os.listdir(STYLES_PATH) if x != '__init__.py']
    _logger.debug(f"Available styles: {available_styles}")
    for stl in available_styles:
        if style.lower() in stl.lower():
            style_dir = stl
            break

    if style_dir is None:
        stylesheet = ""
        raise FileNotFoundError("Style " + style + " does not exists")

    # check if any style_rc was loaded before
    if "style_rc" in sys.modules:
        _logger.info("Found already imported style in sys.modules")

        # use qCleanupResources to remove all resource files
        global style_rc  # noqa
        style_rc.qCleanupResources()

        # remove imported modules
        for x in [module for module in sys.modules if module.startswith("style_rc")]:
            del sys.modules[x]
            del style_rc

        # remove path to previously imported style from sys.path
        for stylepath in [path for path in sys.path if any(style for style in get_available_styles() if style in path)]:
            sys.path.remove(stylepath)
        _logger.debug("Removed all imported styles")

    try:
        _logger.debug("Loading style from directory: " + style_dir)
        old_working_dir = os.getcwd()
        # set style directory
        package_dir = os.path.join(STYLES_PATH, style_dir)
        os.chdir(package_dir)

        # append directory to sys.path and import style_rc
        sys.path.append(package_dir)
        import style_rc  # noqa

        # get palette
        palette = style_rc.palette
        os.chdir(old_working_dir)
    except FileExistsError:
        raise FileNotFoundError("Missing style_rc.py file")

    _logger.info("Style resources imported successfully")

    # Thus, by importing the binary we can access the resources
    package_dir = os.path.basename(PACKAGE_PATH)
    qss_rc_path = ":" + os.path.join(package_dir, QSS_FILE)

    _logger.debug("Reading QSS file in: %s", qss_rc_path)

    # It gets the qss file from compiled style_rc that was import
    # not from the file QSS as we are using resources
    qss_file = QFile(qss_rc_path)

    if qss_file.exists():
        qss_file.open(QFile.ReadOnly | QFile.Text)
        text_stream = QTextStream(qss_file)
        stylesheet = text_stream.readAll()
        _logger.info("QSS file sucessfuly loaded.")
    else:
        stylesheet = ""
        # Todo: check this raise type and add to docs
        raise FileNotFoundError("Unable to find QSS file '{}' "
                                "in resources.".format(qss_rc_path))

    _logger.debug("Checking patches for being applied.")

    # Todo: check execution order for these functions
    # 1. Apply OS specific patches
    stylesheet += _apply_os_patches(palette)

    # 2. Apply binding specific patches
    stylesheet += _apply_binding_patches()

    # 3. Apply binding version specific patches
    stylesheet += _apply_version_patches()

    # 4. Apply palette fix. See issue #139
    _apply_application_patches(palette, QCoreApplication, QPalette, QColor)

    return stylesheet


def load_stylesheet(qt_api="", style='qdarkstyle'):
    """
    Load the stylesheet. Takes care of importing the rc module.

    Args:
        qt_api (str): Qt binding name to set QT_API environment variable.
                      Default is '', i.e PyQt5 the default QtPy binding.
                      Possible values are pyside2, pyqt5.
                      Not case sensitive.

        style (str): Style to use. Default is 'darkblue'

    Returns:
        str: the stylesheet string.
    """

    stylesheet = ""

    if qt_api:
        stylesheet = _load_stylesheet(qt_api=qt_api, style=style)

    else:
        stylesheet = _load_stylesheet(qt_api='pyqt5', style=style)

    return stylesheet


def load_stylesheet_pyside2(style='darkblue'):
    """
    Load the stylesheet for use in a PySide2 application.

    Returns:
        str: the stylesheet string.
    """
    return _load_stylesheet(qt_api='pyside2', style=style)


def load_stylesheet_pyqt5(style='darkblue'):
    """
    Load the stylesheet for use in a PyQt5 application.

    Returns:
        str: the stylesheet string.
    """
    return _load_stylesheet(qt_api='pyqt5', style=style)
