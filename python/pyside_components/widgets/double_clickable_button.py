# -*- coding: utf-8 -*-
from qtpy import QtCore, QtWidgets

class DoubleClickableButtonMixin(object):

    double_clicked = QtCore.Signal()
    
    def mouseDoubleClickEvent(self, e):
        self.double_clicked.emit()
        super(DoubleClickableButtonMixin, self).mouseDoubleClickEvent(e)
        
    def keyPressEvent(self, e):
        return
        

class DoubleClickableButton(DoubleClickableButtonMixin, QtWidgets.QPushButton):
  
    def __init__(self, text='', parent=None):
        super(DoubleClickableButton, self).__init__(text, parent)
        
