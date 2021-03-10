# -*- coding: utf-8 -*-
import sys
from functools import partial
from qtpy import QtCore, QtWidgets
import qtawesome as qta
from pyside_components.widgets.double_clickable_button import DoubleClickableButton
from pyside_components.widgets.text_editable_button import TextEditableButton
from pyside_components.widgets.removable_button import RemovableButton
from pyside_components.widgets.tag_button import TagButton

def print_(s):
    print(s)

def print_button_text(btn):
    print(btn.text())

class TestDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(TestDialog, self).__init__(*args, **kwargs)
        lo = QtWidgets.QVBoxLayout()

        # Deafult push button.
        btn = QtWidgets.QPushButton()
        btn.clicked.connect(partial(print_button_text, btn))
        btn.setText(type(btn).__name__)
        lo.addWidget(btn)

        # Double clickable button.
        btn = DoubleClickableButton()
        btn.clicked.connect(partial(print_, 'single!'))
        btn.double_clicked.connect(partial(print_, 'double!!'))
        btn.setText(type(btn).__name__)
        lo.addWidget(btn)

        # Text editable button.
        btn = TextEditableButton()
        btn.clicked.connect(partial(print_button_text, btn))
        btn.setText(type(btn).__name__)
        lo.addWidget(btn)

        # Removable button
        hlo = QtWidgets.QHBoxLayout()
        self.removable_btn_lo = QtWidgets.QVBoxLayout()
        hlo.addLayout(self.removable_btn_lo)
        btn = RemovableButton()
        btn.clicked.connect(partial(print_button_text, btn))
        btn.closed.connect(partial(print_, 'closed!'))
        btn.setText(type(btn).__name__)
        self.removable_btn_lo.addWidget(btn)

        add_icon = qta.icon('fa5s.plus', color='gray')
        add_btn = QtWidgets.QPushButton()
        add_btn.setStyleSheet('background-color: rgba(1,1,1,0);')
        add_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        add_btn.setIcon(add_icon)
        add_btn.clicked.connect(self.add_removable_button)
        hlo.addWidget(add_btn, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

        lo.addLayout(hlo)

        # Tag button
        self.tag_btn_le = QtWidgets.QLineEdit()
        # self.tag_btn_le.setStyleSheet('border-radius: 5px')
        self.tag_btn_le.setPlaceholderText('Add tag...')
        self.tag_btn_le.editingFinished.connect(self.add_tag_button)
        lo.addWidget(self.tag_btn_le)

        self.tag_btn_lo = QtWidgets.QVBoxLayout()
        btn = TagButton()
        btn.clicked.connect(partial(print_button_text, btn))
        btn.closed.connect(partial(print_, 'closed!'))
        btn.text_changed.connect(partial(print_, 'text changed!!'))
        btn.setText(type(btn).__name__)
        self.tag_btn_lo.addWidget(btn)

        lo.addLayout(self.tag_btn_lo)

        # Spacer
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        lo.addItem(spacer)
        self.setLayout(lo)

    def add_removable_button(self):
        btn = RemovableButton()
        btn.clicked.connect(partial(print_button_text, btn))
        btn.closed.connect(partial(print_, 'closed!'))
        btn.setText(type(btn).__name__)
        self.removable_btn_lo.addWidget(btn)

    def add_tag_button(self):
        text = self.tag_btn_le.text()
        
        if not text:
            return
        
        self.tag_btn_le.setText('')
        btn = TagButton()
        btn.clicked.connect(partial(print_button_text, btn))
        btn.closed.connect(partial(print_, 'closed!'))
        btn.setText(text)
        self.tag_btn_lo.addWidget(btn)

        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = TestDialog()
    dialog.show()
    sys.exit(app.exec_())