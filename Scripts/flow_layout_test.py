# -*- coding: utf-8 -*-
import sys
import codecs
from qtpy import QtCore, QtGui, QtWidgets
from pyside_components.layouts.flow_layout import FlowLayout

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        flowLayout = FlowLayout(self)
        flowLayout.addWidget(QtWidgets.QPushButton("Short"))
        flowLayout.addWidget(QtWidgets.QPushButton("Longer"))
        flowLayout.addWidget(QtWidgets.QPushButton("Different text"))
        flowLayout.addWidget(QtWidgets.QPushButton("More text"))
        flowLayout.addWidget(QtWidgets.QPushButton("Even longer button text"))

        self.setWindowTitle("Flow Layout")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())