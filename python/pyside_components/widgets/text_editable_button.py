# -*- coding: utf-8 -*-
from qtpy import QtCore, QtGui, QtWidgets
from .double_clickable_button import DoubleClickableButton

class TextEditableButton(DoubleClickableButton):

    text_changed = QtCore.Signal()
    
    def __init__(self, text='', parent=None):
        super(DoubleClickableButton, self).__init__(text, parent)
        self.add_lineedit()

    def add_lineedit(self):
        self.lineedit = QtWidgets.QLineEdit(self)
        self.lineedit.setContentsMargins(1,1,1,1)
        self.lineedit.hide()
        self.lineedit.editingFinished.connect(self.set_text)
        self.double_clicked.connect(self.to_editable)

    def resizeEvent(self, e):
        super(TextEditableButton, self).resizeEvent(e)
        self.lineedit.resize(self.size())

    def setText(self, s):
        super(TextEditableButton, self).setText(s)
        self.text_changed.emit()

    def set_text(self):
        text = self.lineedit.text()

        if text:
            self.setText(text)

        self.lineedit.hide() 

    def to_editable(self):
        self.lineedit.setText(self.text())
        self.lineedit.show()
        self.lineedit.selectAll()
        self.lineedit.setFocus()