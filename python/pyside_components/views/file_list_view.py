from qtpy import QtCore, QtGui, QtWidgets
import pyside_components.widgets.path_edit as path_edit

class FileListView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)
        self.lo = QtWidgets.QVBoxLayout()
        self.lo.setContentsMargins(0,0,0,0)
        self.lo.setSpacing(0)
        self.setLayout(self.lo)

        # root dir edit
        self.root_dir_edit = path_edit.DirectoryPathEdit(self)
        self.lo.addWidget(self.root_dir_edit)

        # view
        self.view = QtWidgets.QTreeView()
        self.view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lo.addWidget(self.view)

    def __getattr__(self, attrname):
        attr = getattr(self.view, attrname)
        return attr

    def setModel(self, model):
        self.view.setModel(model)

        
        # header = self.view.header()
        self.view.resizeColumnToContents(0)
        self.view.resizeColumnToContents(1)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def set_root_dir_path(self, root_dir_path):
        model = self.view.model()
        model.set_root_path(root_dir_path)