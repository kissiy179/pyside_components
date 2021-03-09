# -*- coding: utf-8 -*-
from qtpy import QtCore, QtWidgets

class DoubleClickableButton(QtWidgets.QPushButton):

    double_clicked = QtCore.Signal()
    
    def __init__(self, text='', parent=None):
        super(DoubleClickableButton, self).__init__(text, parent)
        
    def mouseDoubleClickEvent(self, e):
        self.double_clicked.emit()
        super(DoubleClickableButton, self).mouseDoubleClickEvent(e)
        
    def keyPressEvent(self, e):
        return
        
