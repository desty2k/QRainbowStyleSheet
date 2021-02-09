#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A customizable style sheet for QtWidgets application.
"""

# Standard library imports
import glob
import os
from setuptools import find_packages, setup

# Package imports
from qrainbowstyle import __doc__ as long_desc
from qrainbowstyle import __version__

install_requires = ['helpdev>=0.6.10', 'qtpy>=1.9', 'PyQtWebEngine']

extras_require = {
    'develop': ['qtsass', 'watchdog'],
    'docs': ['sphinx', 'sphinx_rtd_theme'],
    'example': ['pyqt5', 'pyside2']
}


def remove_all(dir_path, patterns='*.pyc'):
    """Remove all files from `dir_path` matching the `patterns`.

    Args:
        dir_path (str): Directory path.
        patterns (str): Pattern using regex. Defaults to '*.pyc'.
    """

    for pattern in patterns:
        for filename in glob.iglob(dir_path + '/**/' + pattern, recursive=True):
            os.remove(filename)


setup(
    name='qrainbowstyle',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/desty2k/QRainbowStyleSheet',
    license='MIT',
    author='Wojciech Wentland',
    author_email='wojciech.wentland@int.pl',
    description='The most complete customizable stylesheet for Python and Qt applications',
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    python_requires='>=3.5',
    zip_safe=False,  # don't use eggs
    entry_points={"console_scripts": ["qrainbowstyle=qrainbowstyle.__main__:main"]},
    extras_require=extras_require,
    install_requires=install_requires,
    project_urls={
        "Issues": "https://github.com/desty2k/QRainbowStyleSheet/issues",
        "Docs": "https://desty2k.github.io/QRainbowStyleSheet/",
    }
)
