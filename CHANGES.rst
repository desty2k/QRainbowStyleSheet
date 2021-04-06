Changelog
=========

- 0.8.3:
    - Fix setting parent for frameless windows, window modality works now
    - Fix window outside display when moved in maximized mode
    - Fix do not list pycache as style
    - Update example

- 0.8.2:
    - Do not use app event filters in FramelessWindows
      for non Windows OS, fixes 0xC0000005 errors
    - Update PyPI docs and readme
    - Fix moving window not working in frameless messageboxes

- 0.8.1:
    - Fix file with capitalized name not commited to GH
    - Do not use titlebar signal to close window

- 0.8:
    - Refactor code in windows module
    - Add Windows API support
    - Add OS detection
    - Update funcs names
    - Update examples
    - Update scripts to use loggers
    - 0xC0000005 errors are now fixed
    - Regenerate resources

- 0.7.1:
    - Fix windows being deleted after creating them in slots
    - Reduce amount of window flags

- 0.7:
    - Add new color system from qdarkstyle v3
    - Update checkbox icon when checked
    - Update styles using new palette
    - Generate resources
    - Update readme
    - Update preview images
    - Update examples
    - Add slot to connect two markers in GoogleMapsView
    - Fix marker removed after double clicking
    - Remove prints on fade in/out in spinner

- 0.6.6:
    - Add setters for window title and icon
    - Update readme
    - Update OutputLogger
    - Update example2
    - Update loggers names
    - Fix white background when resizing GoogleMapsView

- 0.6.5:
    - Add button getter is FramelessMessageBox
    - GoogleMapsView: Add Python boolean to JS converter
    - GoogleMapsView: Add map events catchers - resizing/loading
    - GoogleMapsView: Add 4 new map settings
    - GoogleMapsView: Add map function: pan to center
    - Update package logger name
    - Fix chdir back to working dir after importing style
    - Update GoogleMapsView example

- 0.6.4:
    - Add vertical and horizontal style pickers
    - Add fadeIn and fadeOut for waitingspinner
    - Change StylePicker name to StylePickerGrid
    - Update frameless mainwindow gif
    - Fix html not loaded when running javascript scripts

- 0.6.3:
    - Add preview gifs
    - Add docs for titlebar
    - Add space between window side and buttons in titlebar
    - Remove getWorkspace titlebar
    - Fix buttons appearing in titlebar even when using darwin style

- 0.6.2:
    - Fix resize handler
    - Add FramelessDialog and FramelessMessageBoxes
    - GoogleMapsView: support for markers and polylines
    - GoogleMapsView: logging Javascript console errors
    - GoogleMapsView: signals for mouse events
    - GoogleMapsView: update example3
    - Add FramelessDialog to style.scss
    - Re-generate resources
    - Replace .pngs with .gif in README in preview section

- 0.6.1:
    - Add QRoundProgressBar
    - Add example for round progress bar
    - Fix error when importing widgets
    - Update README

- 0.6:
    - Add early versions of GoogleMapsView and StylePicker
    - Add docs for new widgets
    - Add example scripts for new widgets
    - Add new preview images
    - Update README

- 0.5.6:
    - Add Resizer module
    - Add rainbowize() and get_available_palettes()
    - Add getters for screen geometry
    - Add setIcons() for titlebar icons
    - Fix updating titlebar buttons' icons after changing stylesheet
    - Move debugging stuff to extras
    - Remove content widget margins for frameless window

- 0.5.5:
    - Add widgets subpackage
    - Add QtWaitingSpinner
    - Update spinner to use qtpy
    - Update spinner to use color from palette
    - Update spinner designer
    - Remove deploy on push with v* tag
    - Fix window flickering when resizing frameless windows
    - Add custom frameless windows resize
    - Remove size grip
    - Update example2

- 0.5.4:
    - Fix copyrights in license
    - Add square icons for close buttons
    - Generate resources

- 0.5.3:
    - Add auto publishing release on successful build
    - Update docs url in setup.py

- 0.5.2:
    - Add auto release to PyPI after build
    - Ignore styles directory in Pylint

-  0.5.1:
    - Update PyPI docs
    - Update badges
    - Fix deploy workflow

-  0.5:
    -  Add build and docs workflows
    -  Add badges to README
    -  Add PyPI deploy workflow
    -  Create first QRainbowStyleSheet release
    -  Upload package to PyPI
    -  Update comments
    -  Update LICENSE and AUTHORS
    -  Update code of conduct version
    -  Remove PyQt4 and Pyside support
    -  Remove old api and deprecated code
    -  Remove Python 2.7 support
    -  Finish migrating docs to GitHub Pages

-  0.4:
    -  Add dependabot
    -  Add Windows and Darwin to tox platforms
    -  Fix preview images in docs
    -  Add auto generating docs on commit
    -  Move builds to Github Actions
    -  Remove Travis-CI config
    -  Remove pyside and pyqt4 from tox

-  0.3:
    -  Change qdarkstyle module name to qrainbowstyle
    -  Generate resources with new prefix

-  0.2:
    -  Add preview images
    -  Add frameless windows
    -  Add new example script
    -  Add NT and Darwin window buttons svg files
    -  Add svg to png generators for window buttons
    -  Update README
    -  Generate resources

-  **0.1**:
    -  Change project name
    -  Add stylesheet for QDial
    -  Add support for multiple styles
    -  Add new palettes: Oceanic, Cyberpunk, DarkOrange, LightOrange
    -  Apply https://github.com/ColinDuquesnoy/QDarkStyleSheet/pull/233
    -  Apply https://github.com/ColinDuquesnoy/QDarkStyleSheet/pull/241
    -  Removed old resources
    -  Generate resources for new styles
