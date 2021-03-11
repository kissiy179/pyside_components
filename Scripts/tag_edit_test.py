# -*- coding: utf-8 -*-
import sys
import codecs
from qtpy import QtCore, QtGui, QtWidgets
from pyside_components.widgets.tag_edit import TagEdit

class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        lo = QtWidgets.QVBoxLayout()
        lo.setContentsMargins(0,0,0,0)
        self.setLayout(lo)
        tag_view = TagEdit()
        lo.addWidget(tag_view)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())