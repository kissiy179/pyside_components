# -*- coding: utf-8 -*-
import os
from qtpy import QtCore, QtGui, QtWidgets
import qtawesome as qta

class Image(QtWidgets.QLabel):

    def __init__(self, path='', scale=1.0, parent=None):
        super(Image, self).__init__(parent)
        self.__path = path
        self.__scale = scale
        self.init_ui()

    def init_ui(self):
        if not os.path.exists(self.__path):
            return

        self.pixmap = QtGui.QPixmap(self.__path)

        if self.scale != 1.0:
            w = self.pixmap.width() * self.__scale
            h = self.pixmap.height() * self.__scale
            self.pixmap = self.pixmap.scaled(w, h)
            
        self.setPixmap(self.pixmap)

    def set_path(self, path):
        self.__path = path
        self.init_ui()

    def scale(self, scale):
        self.__scale = scale
        self.init_ui()
