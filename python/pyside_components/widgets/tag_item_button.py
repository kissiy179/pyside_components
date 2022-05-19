# -*- coding: utf-8 -*-
import sys
import codecs
from qtpy import QtCore, QtGui, QtWidgets
import qtawesome as qta
from ..util import color as color_
from .text_editable_button import TextEditableButtonMixin
from .removable_button import RemovableButtonMixin

tag_item_button_style = '''
{class_name} {{
    background-color: {bg_color};
    color: white;
    border-radius: 4px;
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
    border-radius: 3px;
}}
'''

# class TagItemButton(RemovableButtonMixin, TextEditableButtonMixin, QtWidgets.QPushButton):
class TagItemButton(RemovableButtonMixin, QtWidgets.QPushButton):

    icon_color = 'whitesmoke'

    def __init__(self, text='', parent=None):
        super(TagItemButton, self).__init__(text, parent)
        self.setCheckable(True)
        # self.text_changed.connect(self.set_style)
        self.set_style()

    def set_style(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        color = color_.string_to_color(self.text())
        color_str = 'rgb({},{},{})'.format(*color)
        style_ = tag_item_button_style.format(class_name=type(self).__name__, bg_color=color_str)
        self.style_ = '{}\n{}'.format(self.styleSheet(), style_)
        self.setStyleSheet(self.style_)
