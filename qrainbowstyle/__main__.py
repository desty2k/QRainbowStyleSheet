#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard library imports
import argparse
import sys
from os.path import abspath, dirname

# Third party imports
import helpdev

# Local imports
import qrainbowstyle

sys.path.insert(0, abspath(dirname(abspath(__file__)) + '/..'))


def main():
    """Execute QRainbowStyle helper."""
    parser = argparse.ArgumentParser(description="QRainbowStyle helper. Use the option --all to report bugs",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--information', action='store_true',
                        help="Show information about environment")
    parser.add_argument('-b', '--bindings', action='store_true',
                        help="Show available bindings for Qt")
    parser.add_argument('-a', '--abstractions', action='store_true',
                        help="Show available abstraction layers for Qt bindings")
    parser.add_argument('-d', '--dependencies', action='store_true',
                        help="Show information about dependencies")
    parser.add_argument('-s', '--styles', action='store_true',
                        help="Show available styles")

    parser.add_argument('--all', action='store_true',
                        help="Show all information options at once")

    parser.add_argument('-v', '--version', action='version',
                        version='v{}'.format(qrainbowstyle.__version__))

    # parsing arguments from command line
    args = parser.parse_args()
    no_args = not len(sys.argv) > 1
    info = {}

    if no_args:
        parser.print_help()

    if args.styles:
        print("Available styles: {}".format(qrainbowstyle.getAvailableStyles()))

    if args.information or args.all:
        info.update(helpdev.check_os())
        info.update(helpdev.check_python())

    if args.bindings or args.all:
        info.update(helpdev.check_qt_bindings())

    if args.abstractions or args.all:
        info.update(helpdev.check_qt_abstractions())

    if args.dependencies or args.all:
        info.update(helpdev.check_python_packages(packages='helpdev,qrainbowstyle'))

    helpdev.print_output(info)


if __name__ == "__main__":
    sys.exit(main())
