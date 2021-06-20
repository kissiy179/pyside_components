# -*- coding: utf-8 -*-
from functools import partial
from pprint import pprint
from qtpy import QtCore, QtWidgets
import qtawesome as qta
from .tag_item_button import TagItemButton
from ..layouts.flow_layout import FlowLayout

lineedit_style = '''
QLineEdit {
    border-radius: 5px;
}
'''

def log(s):
    print(s)

class LineEditForAddingTag(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(LineEditForAddingTag, self).__init__(parent)
        self.setMinimumSize(100, 23)
        self.setStyleSheet(lineedit_style)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.editingFinished.connect(self.clear)

        try:
            self.setClearButtonEnabled(True)

        except:
            pass

class TagEdit(QtWidgets.QWidget):

    tags = {}
    tag_buttons = []

    def __init__(self, parent=None):
        super(TagEdit, self).__init__(parent)
        self.init_ui()

    # def clear_layout(self):
    #     dmy_wgt = QtWidgets.QWidget()
    #     dmy_wgt.setLayout(self.layout())
    #     del dmy_wgt

    def init_ui(self):
        hlo = QtWidgets.QHBoxLayout()
        self.setLayout(hlo)        
        
        # Add line edit.
        self.line_edit = LineEditForAddingTag()
        hlo.addWidget(self.line_edit)
        self.line_edit.setPlaceholderText('Add tag...')
        self.line_edit.returnPressed.connect(self.add_tag_from_line_edit) # > add tag
        self.line_edit.returnPressed.connect(self.draw_tag_buttons)

        # Add tag buttons.
        self.tag_lo = QtWidgets.QHBoxLayout()
        self.layout().addLayout(self.tag_lo)
        self.draw_tag_buttons()

        # Add spacer item.
        spc = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        hlo.addItem(spc)

    @staticmethod
    def update_ui(*args, **kwargs):
        
        def outer(func):
            def inner(*args, **kwargs):
                rtn = func(*args, **kwargs)
                return rtn

            return inner

        return outer    

    def clear_tag_buttons(self):
        tags = dict(self.tags)

        for btn in self.tag_buttons:
            # btn.closed.disconnect()
            btn.close()

        self.tags = tags
        self.tag_buttons = []

    def draw_tag_buttons(self, dmy=None):
        self.clear_tag_buttons()
        tags = self.get_tags()

        for tag in tags:
            checked = not self.tags.get(tag)
            btn = TagItemButton(tag)
            self.tag_lo.addWidget(btn)#, QtCore.Qt.AlignLeft)
            btn.setChecked(checked)
            btn.toggled.connect(partial(self.set_tag_checked, tag))
            btn.closed.connect(partial(self.remove_tag, tag))
            btn.text_changed.connect(partial(self.change_tag, tag))
            # btn.text_changed.connect(partial(self.draw_tag_buttons))
            self.tag_buttons.append(btn)

    def add_tag(self, tag):
        if not isinstance(tag, str) or not tag:
            return

        self.tags[tag] = True

    def add_tag_from_line_edit(self):
        tag = self.line_edit.text()
        self.add_tag(tag)
        
    def remove_tag(self, tag):
        if not tag in self.tags:
            return
            
        del self.tags[tag]
        
    def set_tag_checked(self, tag, checked):
        if not tag in self.tags.keys():
            return
            
        self.tags[tag] = not checked
        print(self.get_enabled_tags())

    # @update_ui
    def change_tag(self, old_tag, new_tag):
        if not old_tag in self.tags or new_tag in self.tags:
            return

        checked = self.tags.get(old_tag, True)
        del self.tags[old_tag]
        self.tags[new_tag] = checked
        self.draw_tag_buttons()
        print(self.get_enabled_tags())

    def get_tags(self):
        sorted_ = sorted(self.tags, key=lambda s: s.upper())
        return sorted_

    def get_enabled_tags(self):
        return [tag for tag, enabled in self.tags.items() if enabled]
