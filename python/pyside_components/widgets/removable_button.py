# -*- coding: utf-8 -*-
from qtpy import QtCore, QtWidgets
import qtawesome as qta
from .double_actions_button import DoubleActionsButton, DoubleActionsButtonMixin

removable_btn_style = '''
{class_name} {{
    padding: {padding_left}px {padding_right}px {padding_top}px {padding_bottom}px;
}}
'''

close_btn_style = '''
border: 0px;
padding: 0px;
background-color: rgba(0,0,0,0);
'''
close_btn_style = '''
background-color: rgba(0,0,0,0);
'''

def get_icons(color='gray'):
    '''
    アイコンを作成してdictに格納
    globalでアイコン作成するとスタンドアロンアプリではエラーになるので関数内で作成
    '''
    return {
        'close': qta.icon('fa5s.times-circle', color=color),
    }

class CloseButton(QtWidgets.QPushButton):

    def __init__(self, text='', icon_color='gray', parent=None):
        super(CloseButton, self).__init__(text, parent)
        icons = get_icons(icon_color)
        self.setIcon(icons.get('close'))
        self.setIconSize(QtCore.QSize(14, 14))
        self.setStyleSheet(close_btn_style)

    def keyPressEvent(self, e):
        return

class RemovableButtonMixin(DoubleActionsButtonMixin):

    closed = QtCore.Signal()
    icon_color = 'gray'

    def __init__(self, *args, **kwargs):
        super(RemovableButtonMixin, self).__init__(*args, **kwargs)

    def add_inner_button(self):
        btn = CloseButton(icon_color=self.icon_color, parent=self)
        btn.clicked.connect(self.close)
        return btn

    def close(self):
        super(RemovableButtonMixin, self).close()
        self.closed.emit()

class RemovableButton(RemovableButtonMixin, QtWidgets.QPushButton):

    def __init__(self, text='', parent=None):
        super(RemovableButton, self).__init__(text, parent)
