# -*- coding: utf-8 -*-
import sys
import codecs
from qtpy import QtCore, QtGui, QtWidgets
from pyside_components.layouts.flow_layout import FlowLayout

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.flowLayout = FlowLayout()
        add_btn = QtWidgets.QPushButton('+')
        add_btn.clicked.connect(self.add_button)
        self.flowLayout.addWidget(add_btn)
        self.flowLayout.addWidget(QtWidgets.QPushButton("Short"))
        self.flowLayout.addWidget(QtWidgets.QPushButton("Longer"))
        self.flowLayout.addWidget(QtWidgets.QPushButton("Different text"))
        self.flowLayout.addWidget(QtWidgets.QPushButton("More text"))
        self.flowLayout.addWidget(QtWidgets.QPushButton("Even longer button text"))

        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.flowLayout.addItem(spacer)
        self.setLayout(self.flowLayout)

        self.setWindowTitle("Flow Layout")

    def add_button(self):
        btn = QtWidgets.QPushButton('test')
        self.flowLayout.addWidget(btn)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())