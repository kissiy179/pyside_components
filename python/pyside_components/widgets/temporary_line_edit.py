from qtpy import QtCore, QtWidgets

class TemporaryLineEdit(QtWidgets.QLineEdit):

    __cached_text = ''

    def __init__(self, parent=None):
        super(TemporaryLineEdit, self).__init__(parent)
        self.editingFinished.connect(self.clear)

    def text(self):
        return self.__cached_text

    def clear(self):
        self.__cached_text = super(TemporaryLineEdit, self).text()
        super(TemporaryLineEdit, self).clear()
