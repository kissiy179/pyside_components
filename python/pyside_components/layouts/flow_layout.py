# -*- coding: utf-8 -*-
import sys
from qtpy.QtCore import Qt, QMargins, QPoint, QRect, QSize
from qtpy.QtWidgets import QApplication, QLayout, QPushButton, QSizePolicy, QWidget

'''
以下のサイトから転用/変更
https://kuttsun.blogspot.com/2022/03/pyside-flowlayout.html
'''

class FlowLayout(QLayout):

    def __init__(self, parent=None, margin=0, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)

        self.__itemlist = []
        self.__hSpacing = hspacing
        self.__vSpacing = vspacing

    def __del__(self):
        item = self.takeAt(0)
        while item:
            del item
            item = self.takeAt(0)

    def addItem(self, item):
        self.__itemlist.append(item)

    def count(self):
        return len(self.__itemlist)

    def itemAt(self, index):
        if 0 <= index and index < len(self.__itemlist):
            return self.__itemlist[index]
        return None

    def takeAt(self, index):
        if 0 <= index and index < len(self.__itemlist):
            return self.__itemlist.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.__itemlist:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def doLayout(self, rect, testOnly):
        left, top, right, bottom = self.getContentsMargins()
        effectiveRect = rect.adjusted(+left, +top, -right, -bottom)
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0

        for item in self.__itemlist:
            wid = item.widget()
            spaceX = self.__hSpacing
            if spaceX == -1:
                spaceX = wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.__vSpacing
            if spaceY == -1:
                spaceY = wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)

            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > effectiveRect.right() and lineHeight > 0:
                x = effectiveRect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - effectiveRect.y() + top + bottom

if __name__ == '__main__':

    class MainWindow(QScrollArea):

        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)

            widget = QWidget()
            flowlayout = FlowLayout(widget, 10, 5)
            for i in range(100):
                button = QPushButton("Sample {}".format(i))
                flowlayout.addWidget(button)
            self.setWidgetResizable(True)
            self.setWidget(widget)

    window = MainWindow()
    window.show()
