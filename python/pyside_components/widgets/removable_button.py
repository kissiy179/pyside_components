# -*- coding: utf-8 -*-
from qtpy import QtCore, QtWidgets
import qtawesome as qta

removable_btn_style = '''
RemovableButton {
    padding: %spx %spx %spx %spx;
}
'''

close_btn_style = '''
border: 0px;
padding: 0px;
background-color: rgba(0,0,0,0);
'''

def get_icons(color='gray'):
    '''
    アイコンを作成してdictに格納
    globalでアイコン作成するとスタンドアロンアプリではエラーになるので関数内で作成
    '''
    return {
        'times': qta.icon('fa5s.times', color=color),
    }

class CloseButton(QtWidgets.QPushButton):


    def __init__(self, text='', icon_color='gray', parent=None):
        super(CloseButton, self).__init__(text, parent)
        icons = get_icons(icon_color)
        self.setIcon(icons.get('times'))
        self.setStyleSheet(close_btn_style)

    def keyPressEvent(self, e):
        return

class RemovableButton(QtWidgets.QPushButton):

    closed = QtCore.Signal()
    icon_color = 'gray'

    def __init__(self, text='', parent=None):
        super(RemovableButton, self).__init__(text, parent)
        self.add_close_button()

    def add_close_button(self):
        self.close_btn = CloseButton(icon_color=self.icon_color, parent=self)
        self.close_btn.clicked.connect(self.close)
        btn_size = self.close_btn.sizeHint()
        default_padding = self.style().pixelMetric(QtWidgets.QStyle.PM_ButtonMargin)
        frame_width = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        padding = default_padding - frame_width
        self.setStyleSheet(removable_btn_style % (padding,
                                                  btn_size.width() + padding,
                                                  padding,
                                                  padding))

    def resizeEvent(self, event):
        super(RemovableButton, self).resizeEvent(event)
        btn_size = self.close_btn.sizeHint()
        frame_width = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        self.close_btn.move(self.rect().right() - frame_width - btn_size.width(),
                            (self.rect().bottom() - btn_size.height() + frame_width * 2) /2)

    def close(self):
        super(RemovableButton, self).close()
        self.closed.emit()

