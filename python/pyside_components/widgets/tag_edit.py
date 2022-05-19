# -*- coding: utf-8 -*-
from functools import partial
from pprint import pprint
from qtpy import QtCore, QtWidgets
import qtawesome as qta
from .tag_item_button import TagItemButton
from ..layouts.flow_layout import FlowLayout
from .temporary_line_edit import TemporaryLineEdit

lineedit_style = '''
QLineEdit {
    border-radius: 3px;
}
'''

class LineEditForAddingTag(TemporaryLineEdit):

    def __init__(self, parent=None):
        super(LineEditForAddingTag, self).__init__(parent)
        self.setMinimumSize(100, 23)
        self.setStyleSheet(lineedit_style)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setPlaceholderText('Add tag...')

        try:
            self.setClearButtonEnabled(True)

        except:
            pass

class TagButtonsEdit(QtWidgets.QWidget):

    __buttons = []

    def __init__(self, tags, parent=None):
        super(TagButtonsEdit, self).__init__(parent)
        self.init_ui()

    def clear_ui(self):
        del self.__buttons[:]
        dmy_wgt = QtWidgets.QWidget()
        dmy_wgt.setLayout(self.layout())
        del dmy_wgt

    def init_ui(self):
        self.clear_ui()
        parent = self.parent()
        self.lo = QtWidgets.QHBoxLayout()
        self.lo.setContentsMargins(0,0,0,0)
        self.lo.setSpacing(5)
        self.setLayout(self.lo)
        tags = parent.get_tags()

        for tag_name, enabled in sorted(tags.items()):
            btn = TagItemButton(tag_name)
            btn.setObjectName(tag_name)
            btn.setChecked(not enabled)
            btn.toggled.connect(partial(parent.set_tag_enabled, tag_name))
            btn.closed.connect(partial(parent.remove_tag, tag_name))
            # btn.text_changed.connect(partial(parent.change_tag, tag_name))
            self.lo.addWidget(btn)#, QtCore.Qt.AlignLeft)
            self.__buttons.append(btn)

class TagEdit(QtWidgets.QWidget):

    __tags = {}
    __tag_buttons = []
    updated = QtCore.Signal()

    def __init__(self, parent=None):
        super(TagEdit, self).__init__(parent)
        self.init_ui()
        self.updated.connect(self.update_tag_buttons)
        self.updated.connect(self.log)

    def log(self):
        print(self.__tags)

    def clear_data(self):
        tags = dict(self.__tags)

        for btn in self.__tag_buttons:
            btn.close()

        self.__tags = tags
        self.__tag_buttons = []

    def clear_ui(self):
        dmy_wgt = QtWidgets.QWidget()
        dmy_wgt.setLayout(self.layout())
        del dmy_wgt

    def init_ui(self):
        hlo = QtWidgets.QHBoxLayout()
        hlo.setContentsMargins(2,2,2,2)
        hlo.setSpacing(5)
        self.setLayout(hlo)
        
        # Add line edit.
        self.line_edit = LineEditForAddingTag()
        hlo.addWidget(self.line_edit)
        self.line_edit.editingFinished.connect(self.add_tag_from_line_edit) # > add tag

        # Add tag buttons.
        self.tag_buttons_edit = TagButtonsEdit(self.__tags, parent=self)
        hlo.addWidget(self.tag_buttons_edit)
        self.updated.connect(self.update_tag_buttons)

        # Add spacer item.
        spc = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        hlo.addItem(spc)

    def add_tag(self, tag_name):
        if not isinstance(tag_name, basestring) or not tag_name:
            return

        self.__tags[tag_name] = True
        self.updated.emit()

    def add_tag_from_line_edit(self):
        tag_name = self.line_edit.text()
        self.add_tag(tag_name)
        
    def remove_tag(self, tag_name):
        if not tag_name in self.__tags:
            return
            
        del self.__tags[tag_name]
        self.updated.emit()
        
    def set_tag_enabled(self, tag_name, enabled):
        print(tag_name, enabled)
        if not tag_name in self.__tags.keys():
            return
            
        self.__tags[tag_name] = enabled
        self.updated.emit()

    def change_tag(self, old_tag_name, new_tag_name):
        if not old_tag_name in self.__tags or new_tag_name in self.__tags:
            return

        checked = self.__tags.get(old_tag_name, True)
        del self.__tags[old_tag_name]
        self.__tags[new_tag_name] = checked
        self.updated.emit()

    def get_tags(self):
        return self.__tags

    def set_tags(self, tags):
        self.__tags = tags
        self.updated.emit()

    def get_active_tag_names(self):
        return [tag for tag, enabled in self.__tags.items() if enabled]

    def update_tag_buttons(self):
        self.tag_buttons_edit.init_ui()


'''
import pyside_components; reload(pyside_components)
from pyside_components.widgets.tag_edit import TagEdit

tag_edit = TagEdit()
tag_edit.set_tags({'animations': True, 'characters': False, 'rig': True})
tag_edit.show()
'''