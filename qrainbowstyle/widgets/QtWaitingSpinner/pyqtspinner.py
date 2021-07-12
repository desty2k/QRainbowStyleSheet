"""
The MIT License (MIT)

Copyright (c) 2012-2014 Alexander Turkin
Copyright (c) 2014 William Hallatt
Copyright (c) 2015 Jacob Dawid
Copyright (c) 2016 Luca Weiss
Copyright (c) 2017 fbjorn
Copyright (c) 2020 Wojciech Wentland

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math

from qtpy.QtCore import Qt, QTimer, QRect, Signal, QEvent
from qtpy.QtGui import QColor, QPainter
from qtpy.QtWidgets import QWidget

import qrainbowstyle


class WaitingSpinner(QWidget):
    """QtWaitingSpinner is a highly configurable, custom Qt widget
    for showing "waiting" or "loading" spinner icons in Qt applications,
    e.g. the spinners below are all QtWaitingSpinner widgets
    differing only in their configuration

    Args:
        parent (QWidget): Parent widget.
        centerOnParent (bool): Center on parent widget.
        disableParentWhenSpinning (bool): Disable parent widget when spinning.
        modality (Qt.WindowModality): Spinner modality.
        roundness (float): Lines roundness.
        fade (float): Spinner fade.
        lines (int): Lines count.
        line_length (int): Lines length.
        line_width (int): Lines width.
        radius (int): Spinner radius.
        speed (float): Spinner speed.
    """

    def __init__(self, parent, centerOnParent=True, disableParentWhenSpinning=False,
                 modality=Qt.NonModal, roundness=100., fade=80., lines=20,
                 line_length=10, line_width=2, radius=10, speed=math.pi / 2):
        super().__init__(parent)

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning

        self._color = QColor(0, 0, 0)
        self._roundness = roundness
        self._minimumTrailOpacity = math.pi
        self._trailFadePercentage = fade
        self._oldTrailFadePercentage = fade
        self._revolutionsPerSecond = speed
        self._numberOfLines = lines
        self._lineLength = line_length
        self._lineWidth = line_width
        self._innerRadius = radius
        self._currentCounter = 0

        self._isSpinning = False

        self.fadeInTimer = QTimer()
        self.fadeOutTimer = QTimer()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()
        self.hide()

        self.setWindowModality(modality)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setColor(qrainbowstyle.getCurrentPalette().COLOR_ACCENT_4)

    def paintEvent(self, QPaintEvent):
        self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(Qt.NoPen)
        for i in range(self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength, self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(i, self._currentCounter, self._numberOfLines)
            color = self.currentLineColor(
                distance,
                self._numberOfLines,
                self._trailFadePercentage,
                self._minimumTrailOpacity,
                self._color
            )
            painter.setBrush(color)
            painter.drawRoundedRect(
                QRect(0, - self._lineWidth / 2, self._lineLength, self._lineWidth),
                self._roundness,
                self._roundness,
                Qt.RelativeSize
            )
            painter.restore()

    def changeEvent(self, event: QEvent):
        """Change event handler.

        Args:
            event (QEvent): Event.
        """
        if event.type() == QEvent.StyleChange:
            self.setColor(qrainbowstyle.getCurrentPalette().COLOR_ACCENT_4)

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength(self, length):
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.updateSize()

    def fadeIn(self, time: int = 15):
        self.setTrailFadePercentage(0)
        self.stopFade()
        self.hide()

        self.fadeInTimer = QTimer()
        self.fadeInTimer.timeout.connect(self._on_fadeIn)
        self.fadeInTimer.start(time)

    def _on_fadeIn(self):
        if self.trailFadePercentage < self._oldTrailFadePercentage:
            if self.trailFadePercentage == 0:
                self.show()
            self.setTrailFadePercentage(self.trailFadePercentage + 1)
        else:
            self.fadeInTimer.stop()

    def fadeOut(self, time: int = 15):
        self.show()
        self.stopFade()

        self.fadeOutTimer = QTimer()
        self.fadeOutTimer.timeout.connect(self._on_fadeOut)
        self.fadeOutTimer.start(time)

    def _on_fadeOut(self):
        if self.trailFadePercentage > 0:
            self.setTrailFadePercentage(self.trailFadePercentage - 1)
        else:
            self.hide()
            self.fadeOutTimer.stop()
            self._isFading = False

    def stopFade(self):
        if self.fadeInTimer.isActive():
            self.fadeInTimer.stop()
        if self.fadeOutTimer.isActive():
            self.fadeOutTimer.stop()

    @property
    def color(self):
        return self._color

    @property
    def roundness(self):
        return self._roundness

    @property
    def minimumTrailOpacity(self):
        return self._minimumTrailOpacity

    @property
    def trailFadePercentage(self):
        return self._trailFadePercentage

    @property
    def revolutionsPersSecond(self):
        return self._revolutionsPerSecond

    @property
    def numberOfLines(self):
        return self._numberOfLines

    @property
    def lineLength(self):
        return self._lineLength

    @property
    def lineWidth(self):
        return self._lineWidth

    @property
    def innerRadius(self):
        return self._innerRadius

    @property
    def isSpinning(self):
        return self._isSpinning

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color=Qt.black):
        self._color = QColor(color)

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minimumTrailOpacity = minimumTrailOpacity

    def rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def updateSize(self):
        size = (self._innerRadius + self._lineLength) * 2
        self.setFixedSize(size, size)

    def updateTimer(self):
        self._timer.setInterval(1000 / (self._numberOfLines * self._revolutionsPerSecond))

    def updatePosition(self):
        if self.parentWidget() and self._centerOnParent:
            self.move(
                self.parentWidget().width() / 2 - self.width() / 2,
                self.parentWidget().height() / 2 - self.height() / 2
            )

    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, colorinput):
        color = QColor(colorinput)
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int(math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0))
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color
