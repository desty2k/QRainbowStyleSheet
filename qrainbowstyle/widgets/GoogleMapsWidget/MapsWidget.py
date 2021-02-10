#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MapsView allows to load Google Maps to Qt app.

Usage

.. code-block:: python

    import qrainbowstyle
    import qrainbowstyle.widgets

Work in progress...
"""
import json

from qtpy.QtCore import QObject, Slot, QEvent, Signal, Qt, QUrl
from qtpy.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage
from qtpy.QtNetwork import QNetworkProxyFactory
from qtpy.QtWebChannel import QWebChannel

import qrainbowstyle
import logging

from . import GoogleMapsHtml, OpenStreetMapsHtml


def convertBoolean(value: bool):
    """Convert Python bool to JS boolean.

    Args:
        value (bool): True/False
    """
    if value:
        jvalue = "true"
    else:
        jvalue = "false"
    return jvalue


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

    pageLoaded = Signal()
    pageResized = Signal()
    mapLoaded = Signal()
    tilesLoaded = Signal()

    def __init__(self, parent=None):
        super(CallHandler, self).__init__(parent)
        self._logger = logging.getLogger(self.__class__.__name__)
        self.markers = []

        self._loaded = False
        self._exec_later = []

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

    @Slot()
    def pageIsLoaded(self):
        """Triggered when QWebEngineView finishes loading page.
        Emits pageLoaded signal."""
        self.pageLoaded.emit()

    @Slot()
    def pageIsResized(self):
        """Triggered when map widget is resized. Emits pageResized signal."""
        self.pageResized.emit()

    @Slot()
    def mapIsFullyLoaded(self):
        """Triggered when map finishes loading. Emits mapLoaded signal.
        It may be triggered before showing the map."""
        self.mapLoaded.emit()

    @Slot()
    def tilesAreFullyLoaded(self):
        """Triggered when map finish loading tiles. Emits tilesLoaded signal.
        It is last signal emited after creating MapsView widget."""
        self.tilesLoaded.emit()

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

    def addMarker(self, marker_id, latitude, longitude, options):
        """Creates marker with marker_id id at latitude, longitude.

        Args:
            marker_id (int): Marker id.
            latitude (float): Marker latitude.
            longitude (float): Marker longitude.
            options (dict): Marker options.
        """
        return self.runScript("addMarker({}, {}, {}, {});".format(marker_id, latitude, longitude, json.dumps(options)))

    def addPolyline(self, polyline_id, coordinates: list):
        """Creates polyline between coordinates.

        Args:
            polyline_id (int): Polyline ID.
            coordinates (list): List of coordinates (dicts with "lat" and "lng" keys).
        """
        return self.runScript("addPolyline({}, {});".format(polyline_id, coordinates))

    def addPolylineBetweenMarkers(self, polyline_id, markers_ids: list):
        """Creates polyline between markers.

        Args:
            polyline_id (int): Polyline ID.
            markers_ids (list): List of markers IDs.
        """
        return self.runScript("addPolylineBetweenMarkers({}, {});".format(polyline_id, markers_ids))

    def deletePolyline(self, polyline_id):
        """Delete polyline with provided ID.

        Args:
            polyline_id (int): Polyline ID.
        """
        return self.runScript("deletePolyline({});".format(polyline_id))

    def panToCenter(self):
        """Pan map to center."""
        if self._loaded:
            return self.runScript("panToCenter();")
        else:
            self._exec_later.append(lambda: self.panToCenter())

    def disableMapDragging(self, value):
        """Enable or disable map dragging.

        Args:
            value (bool): Map dragging status.
        """
        if self._loaded:
            return self.runScript("disableMapDragging({});".format(convertBoolean(not value)))
        else:
            self._exec_later.append(lambda: self.disableMapDragging(value))

    def showZoomControl(self, value):
        """Show or hide zoom control widget.

        Args:
            value (bool): Zoom control widget status.
        """
        if self._loaded:
            return self.runScript("showZoomControl({});".format(convertBoolean(value)))
        else:
            self._exec_later.append(lambda: self.showZoomControl(value))

    def disableDoubleClickToZoom(self, value):
        """Enable or disable double click to zoom.

        Args:
            value (bool): Double click to zoom status.
        """
        if self._loaded:
            return self.runScript("disableDoubleClickToZoom({})".format(convertBoolean(value)))
        else:
            self._exec_later.append(lambda: self.disableDoubleClickToZoom(value))

    def disableScrollWheel(self, value):
        """Enable or disable scroll to zoom.

        Args:
            value (bool): Scroll to zoom status.
        """
        if self._loaded:
            return self.runScript("disableScrollWheel({});".format(convertBoolean(not value)))
        else:
            self._exec_later.append(lambda: self.disableScrollWheel(value))

    def enableMarkersDragging(self, value):
        """Enable or disable markers dragging feature.

        Args:
            value (bool): Enable markers dragging.
        """
        if self._loaded:
            return self.runScript("enableMarkersDragging({});".format(convertBoolean(value)))
        else:
            self._exec_later.append(lambda: self.enableMarkersDragging(value))

    def on_loadFinished(self):
        """Set loaded flag to True."""
        self._loaded = True
        for setting in self._exec_later:
            try:
                setting()
            except Exception as e:
                self._logger.warning("Exception while executing setting: {}".format(e))

    def on_loadStarted(self):
        """Set loaded flag to False."""
        self._loaded = False


class MapsPage(QWebEnginePage):
    """QWebEngineView page for handling Javascript console messages."""
    message = Signal(dict)

    def __init__(self, parent=None):
        super(MapsPage, self).__init__(parent)
        self._logger = logging.getLogger(self.__class__.__name__)
        self.setBackgroundColor(Qt.transparent)

    def javaScriptConsoleMessage(self, level, msg, line, source_id):
        """Handle Javascript console messages.

        Args:
            level (int): Logging level.
            msg (str): Message string.
            line (int): Line in code where error occured.
            source_id (str): Element ID.
        """
        self._logger.log(10 * (level + 1), "[{}]: {}".format(line, msg))
        self.message.emit({"level": 10 * (level + 1), "msg": msg, "line": line, "source_id": source_id})


class MapsView(QWebEngineView):
    """Show Google Maps in Qt app."""

    def __init__(self, parent):
        super(MapsView, self).__init__(parent)
        self._logger = logging.getLogger(self.__class__.__name__)

        # Set browser attributes
        QNetworkProxyFactory.setUseSystemConfiguration(False)
        self.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        # Create maps page (it is not needed, but we can handle Javascript console logs)
        self._mapspage = MapsPage(self)
        self.setPage(self._mapspage)

        # Create connection between Javascript and Qt
        self.channel = QWebChannel(self.page())
        self.page().setWebChannel(self.channel)

        # create map events handler and register it as "jshelper" in HTML
        self.handler = CallHandler(self)
        self.handler.runJavascript.connect(self.runScript)
        self.loadFinished.connect(self.handler.on_loadFinished)
        self.loadStarted.connect(self.handler.on_loadStarted)

        self.channel.registerObject("jshelper", self.handler)

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

    def getHandler(self):
        """Returns map event handler."""
        return self.handler

    def enableMarkersDragging(self, value):
        """Enable or disable markers dragging feature.

        Args:
            value (bool): Enable markers dragging.
        """
        self.handler.enableMarkersDragging(value)

    def addMarker(self, marker_id, lat, lng, options=None):
        """Creates marker with marker_id id at latitude, longitude.

        Args:
            marker_id (int): Marker ID.
            lat (float): Marker latitude.
            lng (float): Marker longitude.
            options (dict): Marker options.
        """
        if options is None:
            options = {}
        self.handler.addMarker(marker_id, lat, lng, options)

    def deleteMarker(self, marker_id):
        """Delete marker with ID.

        Args:
            marker_id (int): Marker ID.
        """
        self.handler.deleteMarker(marker_id)

    def updateMarker(self, marker_id, options):
        """Delete marker with ID.

        Args:
            marker_id (int): Marker ID.
            options (dict): Marker options.
        """
        self.handler.updateMarker(marker_id, options)

    def moveMarker(self, marker_id, lat, lng):
        """Move marker to location with (lat, lng).

        Args:
            marker_id (int): Marker ID.
            lat (float): Marker latitude.
            lng (float): Marker longitude.
        """
        self.handler.moveMarker(marker_id, lat, lng)

    def deletePolyline(self, polyline_id):
        """Delete polyline with ID.

        Args:
            polyline_id (int): Polyline ID.
        """
        self.handler.deletePolyline(polyline_id)

    def addPolyline(self, polyline_id, coords: list):
        """Creates polyline using coordinates.

        Args:
            polyline_id (int): Polyline id
            coords (list): List of coordinates (dicts with "lat" and "lng" keys).
        """
        self.handler.addPolyline(polyline_id, coords)

    def addPolylineBetweenMarkers(self, polyline_id, markers: list):
        """Creates polyline using coordinates.

        Args:
            polyline_id (int): Polyline id
            markers (list): List of markers IDs.
        """
        self.handler.addPolylineBetweenMarkers(polyline_id, markers)

    def panToCenter(self):
        """Pan map to center."""
        self.handler.panToCenter()

    def disableMapDragging(self, value):
        """Enable or disable map dragging.

        Args:
            value (bool): Map dragging status.
        """
        self.handler.disableMapDragging(value)

    def showZoomControl(self, value):
        """Show or hide zoom control widget.

        Args:
            value (bool): Zoom control widget status.
        """
        self.handler.showZoomControl(value)

    def disableDoubleClickToZoom(self, value):
        """Enable or disable double click to zoom.

        Args:
            value (bool): Double click to zoom status.
        """
        self.handler.disableDoubleClickToZoom(value)

    def disableScrollWheel(self, value):
        """Enable or disable scroll to zoom.

        Args:
            value (bool): Scroll to zoom status.
        """
        self.handler.disableScrollWheel(value)


class GoogleMapsView(MapsView):

    def __init__(self, parent, api_key):
        super(GoogleMapsView, self).__init__(parent)
        self.api_key = api_key

    def changeEvent(self, event: QEvent):
        """Change event handler.
        Args:
            event (QEvent): Event.
        """
        if event.type() == QEvent.StyleChange:
            self.setHtml(qrainbowstyle.rainbowize(GoogleMapsHtml.html.replace("API_KEY_GOES_HERE", self.api_key)))
        return super().changeEvent(event)


class OpenStreetMapsView(MapsView):

    def __init__(self, parent):
        super(OpenStreetMapsView, self).__init__(parent)

    def changeEvent(self, event: QEvent):
        """Change event handler.
        Args:
            event (QEvent): Event.
        """
        if event.type() == QEvent.StyleChange:
            self.setHtml(qrainbowstyle.rainbowize(OpenStreetMapsHtml.html))
        return super().changeEvent(event)
