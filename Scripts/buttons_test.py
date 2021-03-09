# -*- coding: utf-8 -*-
import sys
from functools import partial
from qtpy import QtCore, QtWidgets
from pyside_components.widgets.double_clickable_button import DoubleClickableButton
from pyside_components.widgets.text_editable_button import TextEditableButton
from pyside_components.widgets.removable_button import RemovableButton

def print_(s):
    print(s)

def print_button_text(btn):
    print(btn.text())

class TestDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(TestDialog, self).__init__(*args, **kwargs)
        lo = QtWidgets.QVBoxLayout()

        # Deafult push button.
        btn = QtWidgets.QPushButton(QtWidgets.QPushButton.__name__)
        btn.clicked.connect(partial(print_button_text, btn))
        lo.addWidget(btn)

        # Double clickable button.
        btn = DoubleClickableButton(DoubleClickableButton.__name__)
        btn.clicked.connect(partial(print_, 'single!'))
        btn.double_clicked.connect(partial(print_, 'double!!'))
        lo.addWidget(btn)

        # Text editable button.
        btn = TextEditableButton(TextEditableButton.__name__)
        btn.clicked.connect(partial(print_button_text, btn))
        lo.addWidget(btn)

        # Removable button
        btn = RemovableButton(RemovableButton.__name__)
        btn.clicked.connect(partial(print_button_text, btn))
        btn.closed.connect(partial(print_, 'closed!'))
        lo.addWidget(btn)

        # Spacer
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        lo.addItem(spacer)
        self.setLayout(lo)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = TestDialog()
    dialog.show()
    sys.exit(app.exec_())