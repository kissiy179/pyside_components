from qtpy import QtCore, QtGui, QtWidgets

class FileListView(QtWidgets.QTreeView):

    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)

    def setModel(self, model):
        super(FileListView, self).setModel(model)
        header = self.header()
        # header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)