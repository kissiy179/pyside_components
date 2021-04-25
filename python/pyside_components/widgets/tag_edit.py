# -*- coding: utf-8 -*-
from functools import partial
from collections import OrderedDict
from qtpy import QtCore, QtWidgets
import qtawesome as qta
from .tag_item_button import TagItemButton
from ..layouts.flow_layout import FlowLayout

lineedit_style = '''
QLineEdit {
    border-radius: 5px;
}
'''

def log_tags(func):

    def wrapper(*args, **kwargs):
        self = args[0]
        func(*args, **kwargs)
        print(self.get_enabled_tags())

    return wrapper

class LineEditForAddingTag(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(LineEditForAddingTag, self).__init__(parent)
        self.setMinimumSize(100, 22)
        self.setStyleSheet(lineedit_style)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

class TagEdit(QtWidgets.QWidget):

    inputed_tag = ''
    placeholder_text = 'Add tag...'
    tags = OrderedDict()

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
                
        for i, tag in enumerate(sorted(self.tags)):
            checked = not self.tags.get(tag)
            btn = TagItemButton(tag)
            btn.setChecked(checked)
            btn.toggled.connect(partial(self.set_tag_checked, i))
            btn.closed.connect(partial(self.remove_tag, i))
            btn.text_changed.connect(partial(self.change_tag, i))
            lo.addWidget(btn)#, QtCore.Qt.AlignLeft)
            
        spc = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        lo.addItem(spc)
        self.setLayout(lo)
        
    def input_tag(self, tag):
        self.inputed_tag = tag
        
    @log_tags
    def add_tag(self):
        if self.inputed_tag == '':
            return
            
        self.tags[self.inputed_tag] = True
        self.inputed_tag = ''
        self.init_ui()
        self.le.setFocus()
        
    @log_tags
    def remove_tag(self, idx):
        tags = self.tags
        tag = list(tags.keys())[idx]
        del self.tags[tag]
        self.init_ui()
        self.le.setFocus()

    @log_tags
    def set_tag_checked(self, idx, checked):
        print(idx)
        tags = self.tags
        tag = list(tags.keys())[idx]
        self.tags[tag] = not checked

    @log_tags
    def change_tag(self, idx, tag):
        tags = self.tags
        crr_tag = list(tags.keys())[idx]
        self.tags = OrderedDict([(tag, v) if k == crr_tag else (k, v) for k, v in tags.items()])
        # self.init_ui()
        # self.le.setFocus()

    def set_placeholder_text(self, text):
        self.placeholder_text = text
        self.le.setPlaceholderText(text)

    def get_tags(self):
        return sorted(self.tags)

    def get_enabled_tags(self):
        return [tag for tag, enabled in self.tags.items() if enabled]
