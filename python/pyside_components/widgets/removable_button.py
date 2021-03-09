# -*- coding: utf-8 -*-
from qtpy import QtCore, QtWidgets
import qtawesome as qta

close_button_style = '''
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

class RemovableButton(QtWidgets.QPushButton):

    closed = QtCore.Signal()

    def __init__(self, text='', parent=None):
        super(RemovableButton, self).__init__(text, parent)
        self.setup_ui()

    def setup_ui(self):
        icons = get_icons('gray')
        self.close_btn = QtWidgets.QPushButton(parent=self)
        self.close_btn.setIcon(icons.get('times'))
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setStyleSheet(close_button_style)

    def close(self):
        self.closed.emit()
        super(RemovableButton, self).close()
