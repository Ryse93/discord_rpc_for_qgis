# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DiscordRPC Plugin for QGIS
                                 A QGIS plugin
 QGIS plugin that enables displaying a Rich Presence in Discord
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-05-27
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Ahhj93
        email                : /
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QTimer
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *

import os.path

from qgis.core import QgsProject
import qgis.core

import time
from pypresence import Presence

class DiscordRPC:
    def __init__(self, iface):
        self.iface = iface
        self.RPC = None
        self.timer = None
        self.start_time = int(time.time())  # Initial start time

    def initGui(self):
        # Initializing the pypresence.Presence instance
        self.RPC = Presence('1112020776099516456')
        self.RPC.connect()

        # Start timer to update RPC every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rpc)
        self.timer.start(5000)  # 5000 ms = 5 s

    def unload(self):
        if self.RPC is not None:
            self.RPC.close()

        # Start timer to update RPC every 5 seconds
        if self.timer is not None:
            self.timer.stop()


    def update_rpc(self):
        # Get the name of the file being modified
        project = QgsProject.instance()
        filename = os.path.basename(project.fileName())

        # Check if the file is open
        if filename != "":
            details = f"Editing {filename}"
            image = "editing"
            text_image = "Editing a file"
        else:
            details = "Idling"
            image = "idling"
            text_image = "Idling"

        # RPC update with filename in state
        self.RPC.update(
            details = details,
            start = self.start_time,
            large_image = image,
            large_text = text_image,
            small_image = "logo",
            small_text = f"QGIS Desktop {get_qgis_version()}",
        )

def get_qgis_version():
    return qgis.core.Qgis.QGIS_VERSION
