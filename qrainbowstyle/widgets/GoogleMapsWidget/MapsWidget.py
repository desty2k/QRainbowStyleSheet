#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""GoogleMapsView allows to load Google Maps to Qt app.

Usage

.. code-block:: python

    import qrainbowstyle
    import qrainbowstyle.widgets

Work in progress...
"""
import json

from qtpy.QtCore import QObject, Slot, QEvent, Signal
from qtpy.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage
from qtpy.QtNetwork import QNetworkProxyFactory
from qtpy.QtWebChannel import QWebChannel

import qrainbowstyle
import logging

from .mapHTML import html


def _replace_api_key(api_key: str):
    return html.replace("API_KEY_GOES_HERE", api_key)


class CallHandler(QObject):
    """Google Maps events handler. Emits signals for
    map, markers, polylines - clicked, doubleClicked, rightClicked,
    moved events.

    Args:
        parent (object): Parent object.
    """
    runJavascript = Signal(str, object)

    mapMoved = Signal(float, float)
    mapClicked = Signal(float, float)
    mapRightClicked = Signal(float, float)
    mapDoubleClicked = Signal(float, float)

    markerMoved = Signal(str, float, float)
    markerClicked = Signal(str, float, float)
    markerDoubleClicked = Signal(str, float, float)
    markerRightClicked = Signal(str, float, float)

    polylineClicked = Signal(str, list)
    polylineRightClicked = Signal(str, list)
    polylineDoubleClicked = Signal(str, list)

    def __init__(self, parent=None):
        super(CallHandler, self).__init__(parent)
        self._logger = logging.getLogger(__name__)
        self.markers = []

    def runScript(self, script, callback=None):
        """Run Javascript code.

        Args:
            script (str): Script to execute.
            callback (callback, optional): Function to handle callback.
        """
        self.runJavascript.emit(script, callback)

    @Slot(float, float)
    def mapIsRightClicked(self, lat, lng):
        """Handle right clicks on map.

        Args:
            lat (float): Event latitude.
            lng (float): Event longitude.
        """
        self._logger.debug("Right clicked on: " + str(lat) + ":" + str(lng))
        self.mapRightClicked.emit(lat, lng)

    @Slot(float, float)
    def mapIsMoved(self, lat, lng):
        """Handle moving the map event.

        Args:
            lat (float): Event latitude.
            lng (float): Event longitude.
        """
        self._logger.debug("Moved, center: " + str(lat) + ":" + str(lng))
        self.mapMoved.emit(lat, lng)

    @Slot(float, float)
    def mapIsClicked(self, lat, lng):
        """Handle clicks on map.

        Args:
            lat (float): Event latitude.
            lng (float): Event longitude.
        """
        self._logger.debug("Clicked on: " + str(lat) + ":" + str(lng))
        self.mapClicked.emit(lat, lng)

    @Slot(float, float)
    def mapIsDoubleClicked(self, lat, lng):
        """Handle double clicks on map.

        Args:
            lat (float): Event latitude.
            lng (float): Event longitude.
        """
        self._logger.debug("Double clicked on: " + str(lat) + ":" + str(lng))
        self.mapDoubleClicked.emit(lat, lng)

    @Slot(str, float, float)
    def markerIsClicked(self, marker_id, lat, lng):
        """Handle clicks on markers.

        Args:
            marker_id (str): Marker id.
            lat (float): Event latitude.
            lng (float): Event longitude.
        """
        self._logger.debug("Marker " + str(marker_id) + " clicked: " + str(lat) + ":" + str(lng))
        self.markerClicked.emit(marker_id, lat, lng)

    @Slot(str, float, float)
    def markerIsRightClicked(self, marker_id, lat, lng):
        """Handle right clicks on markers.

        Args:
            marker_id (str): Marker id.
            lat (float): Event latitude.
            lng (float): Event longitude.
        """
        self._logger.debug("Marker " + str(marker_id) + " right clicked: " + str(lat) + ":" + str(lng))
        self.markerRightClicked.emit(marker_id, lat, lng)

    @Slot(str, float, float)
    def markerIsDoubleClicked(self, marker_id, lat, lng):
        """Handle double clicks on markers.

        Args:
            marker_id (str): Marker id.
            lat (float): Event latitude.
            lng (float): Event longitude.
        """
        self._logger.debug("Marker " + str(marker_id) + " double clicked: " + str(lat) + ":" + str(lng))
        self.markerDoubleClicked.emit(marker_id, lat, lng)
        self.deleteMarker(marker_id)

    @Slot(str, float, float)
    def markerIsMoved(self, marker_id, lat, lng):
        """Handle moving markers.

        Args:
            marker_id (str): Marker id.
            lat (float): Event latitude.
            lng (float): Event longitude.
        """
        self._logger.debug("Marker " + str(marker_id) + " moved to: " + str(lat) + ":" + str(lng))
        self.moveMarker(marker_id, lat, lng)

    @Slot(str, list)
    def polylineIsClicked(self, polyline_id, path: list):
        """Handle clicks on polylines.

        Args:
            polyline_id (str): Polyline id.
            path (list): List of coordinates.
        """
        self._logger.debug("Polyline " + str(polyline_id) + " clicked: " + str(path))
        self.polylineClicked.emit(polyline_id, path)

    @Slot(str, list)
    def polylineIsRightClicked(self, polyline_id, path: list):
        """Handle right clicks on polylines.

        Args:
            polyline_id (str): Polyline id.
            path (list): List of coordinates.
        """
        self._logger.debug("Polyline " + str(polyline_id) + " right clicked: " + str(path))
        self.polylineRightClicked.emit(polyline_id, path)

    @Slot(str, list)
    def polylineIsDoubleClicked(self, polyline_id, path: list):
        """Handle double clicks on polylines.

        Args:
            polyline_id (str): Polyline id.
            path (list): List of coordinates.
        """
        self._logger.debug("Polyline " + str(polyline_id) + " double clicked: " + str(path))
        self.polylineDoubleClicked.emit(polyline_id, path)

    def _updateMarkersCallback(self, markers: list):
        """Callback for loading marker list from QWebEngineView."""
        self.markers = markers

    def loadMarkers(self):
        """Updates markers list."""
        self.runScript("getMarkers();", self._updateMarkersCallback)

    def updateMarker(self, marker_id, args):
        """Update markers parameters."""
        return self.runScript("updateMarker({}, {});".format(marker_id, json.dumps(args)))

    def moveMarker(self, marker_id, latitude, longitude):
        """Move marker to provided latitude and longitude."""
        return self.runScript("moveMarker({}, {}, {});".format(marker_id, latitude, longitude))

    def deleteMarker(self, marker_id):
        """Delete marker with provided ID."""
        return self.runScript("deleteMarker({});".format(marker_id))

    def addMarker(self, marker_id, latitude, longitude):
        """Creates marker with marker_id id at latitude, longitude.

        Args:
            marker_id (float): Marker id.
            latitude (float): Marker latitude.
            longitude (float): Marker longitude.
        """
        return self.runScript("addMarker({}, {}, {});".format(marker_id, latitude, longitude))

    def addPolyline(self, polyline_id, coordinates: list):
        """Creates polyline between coordinates.

        Args:
            polyline_id (str): Polyline ID.
            coordinates (list): List of coordinates (dicts with "lat" and "lng" keys).
        """
        return self.runScript("addPolyline({}, {});".format(polyline_id, coordinates))

    def addPolylineBetweenMarkers(self, polyline_id, markers_ids: list):
        """Creates polyline between markers.

        Args:
            polyline_id (str): Polyline ID.
            markers_ids (list): List of markers IDs.
        """
        return self.runScript("addPolylineBetweenMarkers({}, {});".format(polyline_id, markers_ids))


class GoogleMapsPage(QWebEnginePage):
    """QWebEngineView page for handling Javascript console messages."""

    def __init__(self, parent=None):
        super(GoogleMapsPage, self).__init__(parent)
        self._logger = logging.getLogger(__name__)

    def javaScriptConsoleMessage(self, level, msg, line, source_id):
        """Handle Javascript console messages.

        Args:
            level (int): Logging level.
            msg (str): Message string.
            line (int): Line in code where error occured.
            source_id (str): Element ID.
        """
        self._logger.log(10*(level+1), "[{}]: {}".format(line, msg))


class GoogleMapsView(QWebEngineView):
    """Show Google Maps in Qt app."""

    def __init__(self, parent, api_key):
        super(GoogleMapsView, self).__init__(parent)
        self._logger = logging.getLogger(__name__)

        # Set browser attributes
        QNetworkProxyFactory.setUseSystemConfiguration(False)
        self.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        self.api_key = api_key

        # Create maps page (it is not needed, but we can handle Javascript console logs)
        self._mapspage = GoogleMapsPage(self)
        self.setPage(self._mapspage)

        # Create connection between Javascript and Qt
        self.channel = QWebChannel(self.page())
        self.page().setWebChannel(self.channel)

        # create map events handler and register it as "jshelper" in HTML
        self.handler = CallHandler(self)
        self.handler.runJavascript.connect(self.runScript)
        self.channel.registerObject("jshelper", self.handler)

        # Set HTML
        self.setHtml(qrainbowstyle.rainbowize(_replace_api_key(self.api_key)))

    @Slot(str, object)
    def runScript(self, script, callback):
        """Run Javascript code.

        Args:
            script (str): Script to execute.
            callback (callback, optional): Function to handle callback.
        """
        if callback is None:
            self.page().runJavaScript(script)
        else:
            self.page().runJavaScript(script, callback)

    def addMarker(self, marker_id, lat, lng):
        """Creates marker with marker_id id at latitude, longitude.

        Args:
            marker_id (float): Marker id.
            lat (float): Marker latitude.
            lng (float): Marker longitude.
        """
        self.handler.addMarker(marker_id, lat, lng)

    def addPolyline(self, polyline_id, markers: list):
        """Creates polyline using coordinates.

        Args:
            polyline_id (str): Polyline id
            markers (list): List of coordinates (dicts with "lat" and "lng" keys).
        """
        self.handler.addPolyline(polyline_id, markers)

    def changeEvent(self, event: QEvent):
        """Change event handler.

        Args:
            event (QEvent): Event.
        """
        if event.type() == QEvent.StyleChange:
            self.setHtml(qrainbowstyle.rainbowize(_replace_api_key(self.api_key)))
