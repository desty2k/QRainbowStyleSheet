QRainbowStylesheet
==================

|Build Status| |Docs Status| |Latest PyPI version| |License: MIT|
|License: CC BY 4.0| |Conduct|

The most complete customizable stylesheet for Qt application (Qt5, PySide2,
PyQt5, QtPy, Qt.Py).

Preview
-------

Frameless main window + NT buttons on the right + "Oceanic" style

.. image:: https://raw.githubusercontent.com/desty2k/QRainbowStyleSheet/master/images/frameless_mainwindow_nt_right_oceanic.png

Frameless main window + NT buttons on the right + "Cyberpunk" style

.. image:: https://raw.githubusercontent.com/desty2k/QRainbowStyleSheet/master/images/frameless_mainwindow_nt_right_cyberpunk.png

Frameless main window + Darwin buttons on the left + "DarkOrange" style

.. image:: https://raw.githubusercontent.com/desty2k/QRainbowStyleSheet/master/images/frameless_mainwindow_darwin_left_darkorange.png

Frameless main window + Darwin buttons on the right + "Darkblue" style

.. image:: https://raw.githubusercontent.com/desty2k/QRainbowStyleSheet/master/images/frameless_mainwindow_darwin_right_darkblue.png

Installation
------------


Python
~~~~~~

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


C++
~~~

-  Download/clone the project and copy the following files to your
   application directory (keep the existing directory hierarchy):

    -  **qrainbowstyle/style.qss**
    -  **qrainbowstyle/style.qrc**
    -  **qrainbowstyle/rc/** (the whole directory)


-  Add **qrainbowstyle/style.qrc** to your **.pro file** as follows:

    .. code:: c++

        RESOURCES += qrainbowstyle/style.qrc


-  Load the stylesheet:

    .. code:: c++

        QFile f(":qrainbowstyle/style.qss");

        if (!f.exists())   {
            printf("Unable to set stylesheet, file not found\n");
        }
        else   {
            f.open(QFile::ReadOnly | QFile::Text);
            QTextStream ts(&f);
            qApp->setStyleSheet(ts.readAll());
        }


Note: The ":" in the file name is necessary to define that file as a
resource library. For more information see the discussion
`here <https://github.com/ColinDuquesnoy/QDarkStyleSheet/pull/87>`__.


Available styles
----------------

Currently available styles are:

* oceanic
* cyberpunk
* lightorange
* darkorange
* darkblue (original)

Select style by using keyword argument ``style=``

.. code:: python

    qrainbowstyle.load_stylesheet(style=lightorange)


Usage
-----

If your project already uses QtPy or you need to set it programmatically,
it is far more simple


Frameless windows
~~~~~~~~~~~~~~~~~~
.. code:: python

    import os
    import sys
    import qrainbowstyle
    import qrainbowstyle.windows
    
    from qtpy import QtWidgets
    from qtpy.QtCore import Qt
    
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qrainbowstyle.load_stylesheet(style="oceanic"))

    # Package options
    # qrainbowstyle.align_buttons_left()
    # qrainbowstyle.use_darwin_buttons()
    qrainbowstyle.setAppName("My new application")
    qrainbowstyle.setAppIcon("/path/to/icon.ico")

    # Create frameless mainwindow
    win = qrainbowstyle.windows.FramelessMainWindow()

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
    from PyQt5 import QtWidgets

    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

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
    from PyQt5 import QtWidgets

    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    # setup stylesheet
    app.setStyleSheet(qrainbowstyle.load_stylesheet_pyside2())
    # or in new API
    app.setStyleSheet(qrainbowstyle.load_stylesheet(qt_api='pyside2'))

    # run
    window.show()
    app.exec_()


If you are using Qt.py, which is different from qtpy, you should install
qtpy then set both to the same binding.


*There is an example included in the *example* folder. You can run the
script without installing qrainbowstyle. You only need to have or
PySide2 or PyQt5 installed on your system.*


Building your own style sheet
-----------------------------

Download/clone the project, go to ``qrainbowstyle`` folder then:

1. Create new style in palette.py by subclassing BasePalette. New palette should have unique name, for example ``DeepBluePalette``

2. Override default colors by your own. Example:

    .. code:: python

        class DeepBluePalette(BasePalette):

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

3. Generate resources for your style by running scripts/process_qrc.py

4. Install package by running:

    .. code:: python

        pip install .

5. To use style sheet in your application:

    .. code:: python

        import qrainbowstyle

        app = QApplication(sys.argv)
        app.setStyleSheet(qrainbowstyle.load_stylesheet(style = "deepblue")


What is new?
------------

Starting with new package name, I added possibility to design and build
your own stylesheet. I added few new SVG icons such as title bar icons.
New module with frameless windows has been added.


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
.. |Latest PyPI version| image:: https://img.shields.io/pypi/v/QDarkStyle.svg
   :target: https://pypi.python.org/pypi/QDarkStyle
.. |License: MIT| image:: https://img.shields.io/dub/l/vibe-d.svg?color=lightgrey
   :target: https://opensource.org/licenses/MIT
.. |License: CC BY 4.0| image:: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
   :target: https://creativecommons.org/licenses/by/4.0/
.. |Conduct| image:: https://img.shields.io/badge/code%20of%20conduct-contributor%20covenant-green.svg?style=flat&color=lightgrey
   :target: https://www.contributor-covenant.org/version/2/0/code_of_conduct/
