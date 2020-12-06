from qtpy.QtCore import QObject, Slot, QEvent
from qtpy.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from qtpy.QtWebChannel import QWebChannel


import qrainbowstyle
import logging

from .mapHTML import html


def _replace_api_key(api_key: str):
    return html.replace("API_KEY_GOES_HERE", api_key)


class CallHandler(QObject):
    def __init__(self):
        super(CallHandler, self).__init__()

    @Slot(float, float)
    def logLocation(self, lat, lng):
        print(lat, lng)


class GoogleMapsView(QWebEngineView):
    """Show Google Maps in Qt app."""

    def __init__(self, parent, api_key):
        super(GoogleMapsView, self).__init__(parent)
        self._logger = logging.getLogger(__name__)

        self.api_key = api_key

        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.channel = QWebChannel(self.page())
        self.page().setWebChannel(self.channel)

        self.handler = CallHandler()
        self.channel.registerObject("jshelper", self.handler)

        self.setHtml(qrainbowstyle.rainbowize(_replace_api_key(self.api_key)))

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.StyleChange:
            self.setHtml(qrainbowstyle.rainbowize(_replace_api_key(self.api_key)))
