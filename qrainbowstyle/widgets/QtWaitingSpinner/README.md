# QtWaitingSpinner

[![PyPI version](https://badge.fury.io/py/pyqtspinner.svg)](https://badge.fury.io/py/pyqtspinner)

QtWaitingSpinner is a highly configurable, custom Qt widget for showing "waiting" or "loading" spinner icons in Qt applications, e.g. the spinners below are all QtWaitingSpinner widgets differing only in their configuration:

![waiting spinner](https://github.com/z3ntu/QtWaitingSpinner/blob/gh-pages/waiting-spinners.gif)

### Installation

`pip install pyqtspinner`

### Configuration

The following properties can all be controlled directly through their corresponding setters:

* Color of the widget
* "Roundness" of the lines
* Speed (rotations per second)
* Number of lines to be drawn
* Line length
* Line width
* Radius of the spinner's "dead space" or inner circle
* The percentage fade of the "trail"
* The minimum opacity of the "trail"

### Usage

You can easily ajust spinner settings via `demo.py` file:  

![demo dialog](http://i.imgur.com/dVVSgaS.png)  

Make the spinner you would like to see and press "show init args" button.
It will generate the code snippet which is almost ready-to-use:

```python
WaitingSpinner(
    parent,
    roundness=70.0, opacity=15.0,
    fade=70.0, radius=10.0, lines=12,
    line_length=10.0, line_width=5.0,
    speed=1.0, color=(0, 0, 0)
)
```

As an alternative example, the code below will create a spinner that (1) blocks all user input to the main application for as long as the spinner is active, (2) automatically centers itself on its parent widget every time "start" is called and (3) makes use of the default shape, size and color settings.

```python
spinner = QtWaitingSpinner(self, True, True, Qt.ApplicationModal)
spinner.start() # starts spinning
```


Enjoy!

### Thanks:
to [@fbjorn](https://github.com/fbjorn) for modified version.
to [@z3ntu](https://github.com/z3ntu) for the groundwork.  
to [@snowwlex](https://github.com/snowwlex) for the widget itself.
