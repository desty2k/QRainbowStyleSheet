# -*- coding: utf-8 -*-
"""Script to process QRC files (convert .qrc to _rc.py and .rcc).

The script will attempt to compile the qrc file using the following tools:

    - pyrcc4 for PyQt4 and PyQtGraph (Python)
    - pyrcc5 for PyQt5 and QtPy (Python)
    - pyside-rcc for PySide (Python)
    - pyside2-rcc for PySide2 (Python)
    - rcc for Qt4 and Qt5 (C++)

Delete the compiled files that you don't want to use manually after
running this script.

Links to understand those tools:

    - pyrcc4: http://pyqt.sourceforge.net/Docs/PyQt4/resources.html#pyrcc4
    - pyrcc5: http://pyqt.sourceforge.net/Docs/PyQt5/resources.html#pyrcc5
    - pyside-rcc: https://www.mankier.com/1/pyside-rcc
    - pyside2-rcc: https://doc.qt.io/qtforpython/overviews/resources.html (Documentation Incomplete)
    - rcc on Qt4: http://doc.qt.io/archives/qt-4.8/rcc.html
    - rcc on Qt5: http://doc.qt.io/qt-5/rcc.html

"""

# Standard library imports

import os
import sys
import glob
import logging
import argparse
from subprocess import call

# Third party imports
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Local imports
from qrainbowstyle import PACKAGE_PATH, STYLES_PATH, QRC_FILE, QSS_FILE
from qrainbowstyle.extras import OutputLogger, qt_message_handler
from qrainbowstyle.utils.images import create_images, create_palette_image, generate_qrc_file, create_titlebar_images
from qrainbowstyle.utils.scss import create_qss

from qtpy.QtCore import qInstallMessageHandler


class QSSFileHandler(FileSystemEventHandler):
    """QSS File observer."""

    def __init__(self, parser_args):
        """QSS File observer."""
        super(QSSFileHandler, self).__init__()
        self.args = parser_args

    def on_modified(self, event):
        """Handle file system events."""
        if event.src_path.endswith('.qss'):
            run_process(self.args)
            logging.debug('\n')


def run_process(args):
    """Process qrc files."""

    import inspect
    import qrainbowstyle.palette as source

    palettes = []
    for name, obj in inspect.getmembers(source):
        if inspect.isclass(obj) and issubclass(obj, source.BasePalette) and obj is not source.BasePalette:
            palettes.append(obj)

    logging.debug("Found palettes: " + str(palettes))

    for palette in palettes:
        palette_name = str(palette.__name__)
        logging.debug("Generating files for: " + palette_name)

        # create directory for every style in palette.py
        os.chdir(STYLES_PATH)
        os.makedirs(palette_name, exist_ok=True)
        os.chdir(os.path.join(STYLES_PATH, palette_name))
        open("__init__.py", "w+").close()

        output_dir = os.path.join(STYLES_PATH, palette_name)

        # get paths to output directories for this palette
        images_dir = os.path.join(output_dir, 'images')
        rc_dir = os.path.join(output_dir, 'rc')
        # qss_dir = os.path.join(output_dir, 'qss')

        # create directories
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(rc_dir, exist_ok=True)
        # os.makedirs(qss_dir, exist_ok=True)

        qrc_filepath = os.path.join(output_dir, QRC_FILE)
        qss_filepath = os.path.join(output_dir, QSS_FILE)
        # variables_scss_filepath = os.path.join(qss_dir, VARIABLES_SCSS_FILE)

        # Create palette and resources png images
        logging.debug('Generating palette image ...')
        create_palette_image(palette=palette, path=images_dir)

        logging.debug('Generating images ...')
        create_images(palette=palette, rc_path=rc_dir)

        logging.debug("Generating images for titlebar buttons")
        create_titlebar_images(rc_path=rc_dir, palette=palette)

        logging.debug('Generating qrc ...')
        generate_qrc_file(rc_path=rc_dir, qrc_path=qrc_filepath)

        logging.debug('Converting .qrc to _rc.py and/or .rcc ...')

        for qrc_file in glob.glob('*.qrc'):
            # get name without extension
            filename = os.path.splitext(qrc_file)[0]

            logging.debug(filename + '...')
            ext = '_rc.py'
            ext_c = '.rcc'

            # Create variables SCSS files and compile SCSS files to QSS
            logging.debug('Compiling SCSS/SASS files to QSS ...')
            create_qss(palette=palette, qss_filepath=qss_filepath)

            # creating names
            py_file_pyqt5 = 'pyqt5_' + filename + ext
            py_file_pyqt = 'pyqt_' + filename + ext
            py_file_pyside = 'pyside_' + filename + ext
            py_file_pyside2 = 'pyside2_' + filename + ext
            py_file_qtpy = '' + filename + ext
            py_file_pyqtgraph = 'pyqtgraph_' + filename + ext

            # append palette used to generate this file
            used_palette = "\nfrom qrainbowstyle.palette import " + palette.__name__ + "\npalette = " + palette.__name__ + "\n"

            # calling external commands
            if args.create in ['pyqt', 'pyqtgraph', 'all']:
                logging.debug("Compiling for PyQt4 ...")
                try:
                    call(['pyrcc4', '-py3', qrc_file, '-o', py_file_pyqt])
                    with open(py_file_pyqt, "a+") as f:
                        f.write(used_palette)

                except FileNotFoundError:
                    logging.debug("You must install pyrcc4")

            if args.create in ['pyqt5', 'qtpy', 'all']:
                logging.debug("Compiling for PyQt5 ...")
                try:
                    call(['pyrcc5', qrc_file, '-o', py_file_pyqt5])
                    with open(py_file_pyqt5, "a+") as f:
                        f.write(used_palette)
                except FileNotFoundError:
                    logging.debug("You must install pyrcc5")

            if args.create in ['pyside', 'all']:
                logging.debug("Compiling for PySide ...")
                try:
                    call(['pyside-rcc', '-py3', qrc_file, '-o', py_file_pyside])
                    with open(py_file_pyside, "a+") as f:
                        f.write(used_palette)
                except FileNotFoundError:
                    logging.debug("You must install pyside-rcc")

            if args.create in ['pyside2', 'all']:
                logging.debug("Compiling for PySide 2...")
                try:
                    call(['pyside2-rcc', '-py3', qrc_file, '-o', py_file_pyside2])
                    with open(py_file_pyside2, "a+") as f:
                        f.write(used_palette)
                except FileNotFoundError:
                    logging.debug("You must install pyside2-rcc")

            if args.create in ['qtpy', 'all']:
                logging.debug("Compiling for QtPy ...")
                # special case - qtpy - syntax is PyQt5
                with open(py_file_pyqt5, 'r') as file:
                    filedata = file.read()

                # replace the target string
                filedata = filedata.replace('from PyQt5', 'from qtpy')

                with open(py_file_qtpy, 'w+') as file:
                    # write the file out again
                    file.write(filedata)

                if args.create not in ['pyqt5']:
                    os.remove(py_file_pyqt5)

            if args.create in ['pyqtgraph', 'all']:
                logging.debug("Compiling for PyQtGraph ...")
                # special case - pyqtgraph - syntax is PyQt4
                with open(py_file_pyqt, 'r') as file:
                    filedata = file.read()

                # replace the target string
                filedata = filedata.replace('from PyQt4', 'from pyqtgraph.Qt')

                with open(py_file_pyqtgraph, 'w+') as file:
                    # write the file out again
                    file.write(filedata)


def main(arguments):
    """Process QRC files."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--qrc_dir',
                        default=PACKAGE_PATH,
                        type=str,
                        help="QRC file directory, relative to current directory.",)
    parser.add_argument('--create',
                        default='qtpy',
                        choices=['pyqt', 'pyqt5', 'pyside', 'pyside2', 'qtpy', 'pyqtgraph', 'qt', 'qt5', 'all'],
                        type=str,
                        help="Choose which one would be generated.")
    parser.add_argument('--watch', '-w',
                        action='store_true',
                        help="Watch for file changes.")

    args = parser.parse_args(arguments)

    if args.watch:
        path = PACKAGE_PATH
        observer = Observer()
        handler = QSSFileHandler(parser_args=args)
        observer.schedule(handler, path, recursive=True)
        try:
            logging.debug('Watching QSS file for changes...Press Ctrl+C to exit')
            observer.start()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        run_process(args)


if __name__ == '__main__':
    logger = OutputLogger()
    qInstallMessageHandler(qt_message_handler)
    sys.exit(main(sys.argv[1:]))
