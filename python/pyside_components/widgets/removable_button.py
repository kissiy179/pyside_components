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

    def __init__(self, text='', parent=None):
        super(CloseButton, self).__init__(text, parent)
        icons = get_icons('gray')
        self.setIcon(icons.get('times'))
        self.setStyleSheet(close_btn_style)

    def keyPressEvent(self, e):
        return

class RemovableButton(QtWidgets.QPushButton):

    closed = QtCore.Signal()

    def __init__(self, text='', parent=None):
        super(RemovableButton, self).__init__(text, parent)
        self.add_close_button()

    def add_close_button(self):
        self.close_btn = CloseButton(parent=self)
        self.close_btn.clicked.connect(self.close)
        btn_size = self.close_btn.sizeHint()
        default_padding = self.style().pixelMetric(QtWidgets.QStyle.PM_ButtonMargin)
        self.setStyleSheet(removable_btn_style % (default_padding,
                                                  btn_size.width() + default_padding,
                                                  default_padding,
                                                  default_padding))

    def resizeEvent(self, event):
        super(RemovableButton, self).resizeEvent(event)
        btn_size = self.close_btn.sizeHint()
        frame_width = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        self.close_btn.move(self.rect().right() - frame_width - btn_size.width(),
                            (self.rect().bottom() - btn_size.height() + frame_width * 2) /2)

    def close(self):
        super(RemovableButton, self).close()
        self.closed.emit()

