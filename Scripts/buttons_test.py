import sys
from functools import partial
from qtpy import QtCore, QtWidgets
from pyside_components.widgets.double_clickable_button import DoubleClickableButton

def print_(s):
    print(s)

class TestDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(TestDialog, self).__init__(*args, **kwargs)
        lo = QtWidgets.QVBoxLayout()

        # Double clickable button.
        btn = DoubleClickableButton(DoubleClickableButton.__name__)
        btn.clicked.connect(partial(print_, 'single!'))
        btn.double_clicked.connect(partial(print_, 'double!!'))
        lo.addWidget(btn)

        self.setLayout(lo)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = TestDialog()
    dialog.show()
    sys.exit(app.exec_())