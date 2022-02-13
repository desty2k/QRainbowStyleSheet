QRainbowStyleSheet
==================

|Latest PyPI version| |Supported python versions| |Build Status| |Docs Status| |License: MIT|
|License: CC BY 4.0| |Conduct|

The most complete customizable stylesheet for Qt application (PySide2,
PyQt5, QtPy, Qt.Py).

Preview
-------

From version v0.8 qrainbowstyle.windows module supports native Windows calls.
Features:

    - Borders snapping
    - Minimize, restore, close animations
    - Size grips on borders
    - Frame shadow
    - Aero shake

On Linux and Darwin qrainbowstyle will load class with its own implementation of these features.
Due to a bug in Qt, window minimizing is not supported on MacOS.


Frameless windows
~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/desty2k/QRainbowStyleSheet/master/images/frameless_window_v3.png


Installation
------------

From PyPI: Get the latest stable version of ``qrainbowstyle`` package using
*pip* (preferable):

    .. code:: bash

        pip install qrainbowstyle


From code: Download/clone the project, go to ``qrainbowstyle`` folder then:

-  You can use the *setup* script and pip install.

    .. code:: bash

        pip install .


-  Or, you can use the *setup* script with Python:

    .. code:: bash

        python setup.py install


Usage
-----


Frameless windows
~~~~~~~~~~~~~~~~~~
.. code:: python

    import os
    import sys
    import qrainbowstyle
    import qrainbowstyle.windows

    from qtpy.QtWidgets import QApplication
    from qtpy.QtCore import Qt

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet(style="oceanic"))

    # Package options
    # qrainbowstyle.alignButtonsLeft()
    # qrainbowstyle.userDarwinButtons()
    qrainbowstyle.setAppName("My new application")
    qrainbowstyle.setAppIcon("/path/to/icon.ico")

    # Create frameless mainwindow
    win = qrainbowstyle.windows.FramelessWindow()

    # Example of using signals
    win.closeClicked.connect(lambda: print("Close clicked!"))

    # Create content widget and pass reference to main window
    widget = SomeWidget(win)

    # Add widget to main window and show it
    win.addContentWidget(widget)
    win.show()

    sys.exit(app.exec())


Style sheet
~~~~~~~~~~~~
.. code:: python

    import os
    import sys
    import qrainbowstyle

    # set the environment variable to use a specific wrapper
    # it can be set to pyqt, pyqt5, or pyside2
    # you do not need to use QtPy to set this variable
    os.environ['QT_API'] = 'pyqt5'

    # import from QtPy instead of doing it directly
    # note that QtPy always uses PyQt5 API
    from qtpy import QtWidgets

    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    # setup stylesheet
    # the default system in qrainbowstyle uses qtpy environment variable
    app.setStyleSheet(qrainbowstyle.load_stylesheet())

    # run
    window.show()
    app.exec_()


If you are using PyQt5 directly, see the complete example

.. code:: python

    import sys
    import qrainbowstyle
    from PyQt5.QtWidgets import QApplication, QMainWindow

    # create the application and the main window
    app = QApplication(sys.argv)
    window = QMainWindow()

    # setup stylesheet
    app.setStyleSheet(qrainbowstyle.load_stylesheet_pyqt5())
    # or in new API
    app.setStyleSheet(qrainbowstyle.load_stylesheet(qt_api='pyqt5'))

    # run
    window.show()
    app.exec_()


Here is an example using PySide2

.. code:: python

    import sys
    import qrainbowstyle
    from Pyside2.QtWidgets import QApplication, QMainWindow

    # create the application and the main window
    app = QApplication(sys.argv)
    window = QMainWindow()

    # setup stylesheet
    app.setStyleSheet(qrainbowstyle.load_stylesheet_pyside2())
    # or in new API
    app.setStyleSheet(qrainbowstyle.load_stylesheet(qt_api='pyside2'))

    # run
    window.show()
    app.exec_()


If you are using Qt.py, which is different from qtpy, you should install
qtpy then set both to the same binding.


Available styles
----------------

Currently available styles are:

* Oceanic
* QDarkStyle3
* QDarkstyle3Light
* LightOrange
* DarkOrange
* QDarkStyle (original)

Select style by using ``style=`` keyword argument

.. code:: python

    qrainbowstyle.load_stylesheet(style="lightorange")


Widgets
-------

In v0.6 I added a few new widgets which automatically load colors from current
stylesheet's palette.


GoogleMapsView
~~~~~~~~~~~~~~

GoogleMapsView allows to load Google Maps to application. Supports creating markers and polylines.
Call handler captures all map/markers/polylines actions such as map move or marker click/double click.

.. image:: https://raw.githubusercontent.com/desty2k/QRainbowStyleSheet/master/images/frameless_mainwindow_google_maps_example.png


StylePicker
~~~~~~~~~~~

StylePicker is small widget used to change stylesheet without restarting application.
Only styles generated by QRainbowStyle are supported. Widget is available in 3 versions: horizontal, vertical and grid.

.. image:: https://raw.githubusercontent.com/desty2k/QRainbowStyleSheet/master/images/frameless_mainwindow_color_picker_example.png


QRoundProgressBar
~~~~~~~~~~~~~~~~~

Modified version of https://github.com/ozmartian/QRoundProgressBar.
I replaced PyQt5 imports with qtpy and fixed widget background.

.. image:: https://raw.githubusercontent.com/desty2k/QRainbowStyleSheet/master/images/frameless_mainwindow_round_progress_bar.png


QtWaitingSpinner
~~~~~~~~~~~~~~~~~

Modified version of https://github.com/fbjorn/QtWaitingSpinner. Added fade out and fade in.
Spinner designer can be found in `qrainbowstyle/widgets/QtWaitingSpinner/designer.py`

.. image:: https://raw.githubusercontent.com/desty2k/QRainbowStyleSheet/master/images/waiting_spinner_designer.png


Building your own style sheet
-----------------------------

Download/clone the project, go to ``qrainbowstyle`` folder then:

1. Create new style in palette.py by subclassing BasePalette. New palette should have unique name, for example ``DeepBluePalette``

2. Override default colors by your own. Example:

    .. code:: python

        class DeepBluePalette(BasePalette):
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

3. Generate resources for your style by running scripts/process_qrc.py

4. Install package by running:

    .. code:: python

        pip install .

5. To use style sheet in your application:

    .. code:: python

        import qrainbowstyle

        app = QApplication(sys.argv)
        app.setStyleSheet(qrainbowstyle.load_stylesheet(style="deepblue")


What is new?
------------

Starting with new package name, I added frameless widnows and possibility to
design your own stylesheet. I added few new SVG icons such as title bar icons.

- 0.6 - widget subpackage
- 0.8 - Windows API support
- 0.9 - modern style for frameless windows, full support for new color system


Changelog
---------

Please, see `CHANGES <CHANGES.rst>`__ file.


License
-------

This project is licensed under the MIT license. Images contained in this
project are licensed under CC-BY license.

For more information see `LICENSE <LICENSE.rst>`__ file.


Authors
-------

For more information see `AUTHORS <AUTHORS.rst>`__ file.


Contributing
------------

Most widgets have been styled. If you find a widget that has not been
style, just open an issue on the issue tracker or, better, submit a pull
request.

If you want to contribute, see `CONTRIBUTING <CONTRIBUTING.rst>`__ file.

.. |Build Status| image:: https://github.com/desty2k/QRainbowStyleSheet/workflows/build/badge.svg
   :target: https://github.com/desty2k/QRainbowStyleSheet/actions?workflow=build
.. |Docs Status| image:: https://github.com/desty2k/QRainbowStyleSheet/workflows/docs/badge.svg
   :target: https://desty2k.github.io/QRainbowStyleSheet/
.. |Latest PyPI version| image:: https://img.shields.io/pypi/v/QRainbowStyle.svg
   :target: https://pypi.org/project/QRainbowStyle/
.. |Supported python versions| image:: https://img.shields.io/pypi/pyversions/QRainbowStyle.svg
   :target: https://pypi.org/project/QRainbowStyle/
.. |License: MIT| image:: https://img.shields.io/dub/l/vibe-d.svg?color=lightgrey
   :target: https://opensource.org/licenses/MIT
.. |License: CC BY 4.0| image:: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
   :target: https://creativecommons.org/licenses/by/4.0/
.. |Conduct| image:: https://img.shields.io/badge/code%20of%20conduct-contributor%20covenant-green.svg?style=flat&color=lightgrey
   :target: https://www.contributor-covenant.org/version/2/0/code_of_conduct/
