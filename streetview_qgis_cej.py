# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Streetview_qgis_cej
                                 A QGIS plugin
 Streetview_qgis_cej
 Create Plugin By: https://github.com/Genroy
                              -------------------
        begin                : 2025-05-01
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Thamoon Kedkaew (CeJ)
        Author               : Thamoon Kedkaew (CeJ)
        email                : pongsakornche@gmail.com
 ***************************************************************************/
"""
from qgis.PyQt import QtWidgets, QtWebEngineWidgets, QtCore, QtGui
from qgis.gui import QgsMapToolEmitPoint
from qgis.core import *

class StreetViewDockWidget(QtWidgets.QDockWidget):
    def __init__(self, iface, api_key):
        super().__init__("Street View (Interactive)")
        self.iface = iface
        self.api_key = api_key
        
        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.setWidget(self.webview)
        
        iface.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        
        self.map_tool = QgsMapToolEmitPoint(iface.mapCanvas())
        self.map_tool.canvasClicked.connect(self.show_street_view)
        iface.mapCanvas().setMapTool(self.map_tool)

    def show_street_view(self, point, button):
        crs_src = self.iface.mapCanvas().mapSettings().destinationCrs()
        crs_dest = QgsCoordinateReferenceSystem(4326)
        transform = QgsCoordinateTransform(crs_src, crs_dest, QgsProject.instance())
        transformed_point = transform.transform(point)
        
        lat = transformed_point.y()
        lon = transformed_point.x()
        
        html = f"""
        <!DOCTYPE html>
        <html>
          <head>
            <title>Street View</title>
            <style> html, body, #street-view {{ height: 100%; margin: 0; padding: 0; }} </style>
            <script src="https://maps.googleapis.com/maps/api/js?key={self.api_key}"></script>
            <script>
              function init() {{
                var panorama = new google.maps.StreetViewPanorama(
                  document.getElementById('street-view'),
                  {{
                    position: {{lat: {lat}, lng: {lon}}},
                    pov: {{heading: 165, pitch: 0}},
                    zoom: 1
                  }});
              }}
              window.onload = init;
            </script>
          </head>
          <body>
            <div id="street-view"></div>
          </body>
        </html>
        """
        self.webview.setHtml(html)

class StreetViewQGISCej:
    def __init__(self, iface):
        self.iface = iface
        self.widget = None
        self.action = None
        
    def initGui(self):
        self.action = QtWidgets.QAction("เปิดแล้วทำงานไว!", self.iface.mainWindow())
        self.action.triggered.connect(self.open_street_view)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Street View Plugin", self.action)

    def unload(self):
        if self.action:
            self.iface.removePluginMenu("&Street View Plugin", self.action)
            self.iface.removeToolBarIcon(self.action)
        if self.widget:
            self.iface.removeDockWidget(self.widget)
            self.widget = None

    def open_street_view(self):
        if not self.widget:
            api_key = 'AIzaSyDpCovemQ8nDjZfe5am3WexZSH_OmsR1ZI'
            self.widget = StreetViewDockWidget(self.iface, api_key)
        self.widget.show()

