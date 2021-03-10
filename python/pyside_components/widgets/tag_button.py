# -*- coding: utf-8 -*-
import codecs
from qtpy import QtCore, QtGui, QtWidgets
import qtawesome as qta
from .text_editable_button import TextEditableButton
from .removable_button import RemovableButton

tagbutton_style = '''
TagButton {
    background-color: %s;
    color: white;
    border-radius: 5px;
}
TagButton:hover {
    background-color: rgb(110,110,110);
    color: white;
    border: black 2px;
}
TagButton:pressed {
    background-color: rgb(45,45,45);
    color: white;
    border: black 2px;
}
TagButton:checked {
    background-color: rgb(55,55,55);
    color: gray; border: black 2px;
}
TagButton:checked:hover {
    background-color: rgb(80,80,80);
    color: gray; border: black 2px;
}

QLineEdit {
    border-radius: 4px;
}
'''

def char_to_color(c):
    hex_code = codecs.encode(c[0].lower(), 'hex')
    col_num = eval('0x{}'.format(hex_code))
    return col_num

def string_to_color(s):
    s = s if s else 'z'
    s = s.ljust(3, s[0])
    color = [char_to_color(i) for i in s[:3]]
    n = 2
    max_ = max(color)
    min_ = min(color)
    
    if max_ - min_ <= 20:
        color[0] = min(255, color[0] * n)
        
    return color

class TagButton(RemovableButton, TextEditableButton):

    icon_color = 'lightgray'

    def __init__(self, text='', parent=None):
        super(TagButton, self).__init__(text, parent)
        self.setCheckable(True)
        self.text_changed.connect(self.set_style)
        self.style_ = '{}\n{}'.format(self.styleSheet(), tagbutton_style)

    def set_style(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        color = string_to_color(self.text())
        color_str = 'rgb({},{},{})'.format(*color)
        self.setStyleSheet(self.style_ % color_str)