# -*- coding: utf-8 -*-
from qtpy import QtCore, QtGui, QtWidgets
from .double_clickable_button import DoubleClickableButtonMixin

class TextEditableButtonMixin(DoubleClickableButtonMixin):
    
    text_changed = QtCore.Signal(str)
    
    def __init__(self, *args, **kwargs):
        super(TextEditableButtonMixin, self).__init__(*args, **kwargs)
        self.add_lineedit()

    def add_lineedit(self):
        self.lineedit = QtWidgets.QLineEdit(self)
        self.lineedit.setContentsMargins(1,1,1,1)
        self.lineedit.hide()
        self.lineedit.editingFinished.connect(self.set_text)
        self.double_clicked.connect(self.to_editable)

    def resizeEvent(self, e):
        super(TextEditableButtonMixin, self).resizeEvent(e)
        self.lineedit.resize(self.size())

    def setText(self, s):
        super(TextEditableButtonMixin, self).setText(s)
        self.text_changed.emit(self.text())

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

class TextEditableButton(TextEditableButtonMixin, QtWidgets.QPushButton):
    
    def __init__(self, text='', parent=None):
        super(TextEditableButton, self).__init__(text, parent)
