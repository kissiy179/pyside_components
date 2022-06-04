from qtpy import QtCore, QtGui, QtWidgets
import pyside_components.widgets.path_edit as path_edit

class FileListView(QtWidgets.QTreeView):

    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def setModel(self, model):
        super(FileListView, self).setModel(model)
        column_count = model.columnCount()
                
        for i in range(column_count):
            self.resizeColumnToContents(i)
            # header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    def set_root_dir_path(self, root_dir_path):
        model = self.model()
        model.set_root_path(root_dir_path)