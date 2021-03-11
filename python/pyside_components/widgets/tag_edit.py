# -*- coding: utf-8 -*-
from functools import partial
from qtpy import QtCore, QtWidgets
import qtawesome as qta
from .tag_item_button import TagItemButton
from ..layouts.flow_layout import FlowLayout

lineedit_style = '''
QLineEdit {
    border-radius: 5px;
}
'''

class LineEditForAddingTag(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(LineEditForAddingTag, self).__init__(parent)
        self.setMinimumSize(100, 22)
        self.setStyleSheet(lineedit_style)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

class TagEdit(QtWidgets.QWidget):

    inputed_tag = ''
    placeholder_text = 'Add tag...'
    tags = {}

    def __init__(self, parent=None):
        super(TagEdit, self).__init__(parent)
        self.init_ui()

    def clear_layout(self):
        dmy_wgt = QtWidgets.QWidget()
        dmy_wgt.setLayout(self.layout())

    def init_ui(self):
        self.clear_layout()
        lo = QtWidgets.QHBoxLayout()
        # lo = FlowLayout()
        
        self.le = LineEditForAddingTag()
        self.le.textChanged.connect(self.input_tag)
        self.le.editingFinished.connect(self.add_tag)
        self.le.setPlaceholderText(self.placeholder_text)
        lo.addWidget(self.le)
                
        for tag in sorted(self.tags):
            checked = not self.tags.get(tag)
            btn = TagItemButton(tag)
            btn.setChecked(checked)
            btn.toggled.connect(partial(self.set_tag_checked, tag))
            btn.closed.connect(partial(self.remove_tag, tag))
            lo.addWidget(btn)#, QtCore.Qt.AlignLeft)
            
        spc = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        lo.addItem(spc)
        self.setLayout(lo)
        
    def input_tag(self, tag):
        self.inputed_tag = tag
        
    def add_tag(self):
        if self.inputed_tag == '':
            return
            
        self.tags[self.inputed_tag] = True
        self.inputed_tag = ''
        self.init_ui()
        self.le.setFocus()
        
    def remove_tag(self, tag):
        if not tag in self.tags.keys():
            return
            
        del self.tags[tag]
        
    def set_tag_checked(self, tag, checked):
        if not tag in self.tags.keys():
            return
            
        self.tags[tag] = not checked
        print self.get_enabled_tags()

    def set_placeholder_text(self, text):
        self.placeholder_text = text
        self.le.setPlaceholderText(text)

    def get_tags(self):
        return sorted(self.tags)

    def get_enabled_tags(self):
        return [tag for tag, enabled in self.tags.items() if enabled]
