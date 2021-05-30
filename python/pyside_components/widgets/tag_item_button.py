# -*- coding: utf-8 -*-
import sys
import codecs
from qtpy import QtCore, QtGui, QtWidgets
import qtawesome as qta
from .text_editable_button import TextEditableButtonMixin
from .removable_button import RemovableButtonMixin

tag_item_button_style = '''
{class_name} {{
    background-color: {bg_color};
    color: white;
    border-radius: 5px;
}}
{class_name}:hover {{
    background-color: rgb(110,110,110);
    color: white;
    border: black 2px;
}}
{class_name}:pressed {{
    background-color: rgb(45,45,45);
    color: white;
    border: black 2px;
}}
{class_name}:checked {{
    background-color: rgb(55,55,55);
    color: gray; border: black 2px;
}}
{class_name}:checked:hover {{
    background-color: rgb(80,80,80);
    color: gray; border: black 2px;
}}

QLineEdit {{
    border-radius: 4px;
}}
'''

def char_to_color(c):
    if sys.version.startswith('3'):
        hex_code = codecs.encode(bytes(c, 'utf-8'), 'hex-codec')

    else:
        hex_code = codecs.encode(c.lower(), 'hex')
        
    col_num = int(hex_code, 16)    
    return col_num

def string_to_color(s, correction=40):
    s = s if s else 'z'
    s = s.ljust(3, '0')
    color = [char_to_color(i) for i in s[:3]]
    avg = sum(color) / len(color)

    if avg < correction:
        sub = correction - avg
        color = [min(255, n + sub) for n in color]

    max_ = max(color)
    min_ = min(color)
    
    if max_ - min_ <= 255:
        maxidx = color.index(max_)
        minidx = color.index(min_)
        color[maxidx] = min(255, max_ + correction)
        color[minidx] = max(0, min_ - correction)
        
    return color

class TagItemButton(RemovableButtonMixin, TextEditableButtonMixin, QtWidgets.QPushButton):

    icon_color = 'whitesmoke'

    def __init__(self, text='', parent=None):
        super(TagItemButton, self).__init__(text, parent)
        self.setCheckable(True)
        # self.text_changed.connect(self.set_style)
        self.set_style()

    def set_style(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        color = string_to_color(self.text())
        color_str = 'rgb({},{},{})'.format(*color)
        style_ = tag_item_button_style.format(class_name=type(self).__name__, bg_color=color_str)
        self.style_ = '{}\n{}'.format(self.styleSheet(), style_)
        self.setStyleSheet(self.style_)
