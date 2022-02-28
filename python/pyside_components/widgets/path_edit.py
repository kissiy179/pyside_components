# -*- coding: utf-8 -*-
import os
import inspect
from qtpy import QtWidgets, QtCore
import qtawesome as qta

dir_icon = qta.icon('fa5s.folder', color='lightgray')

def getOpenFileName(parent, dir='', filter=''):
    '''
    QtWidgets.QFileDialog.getOpenFileName が inspect.argspec に通らないので関数でラップ
    '''
    file_obj = QtWidgets.QFileDialog.getOpenFileName(parent, dir=dir, filter=filter)

    if file_obj:
        return file_obj[0]

    return ''

def getExistingDirectory(parent, dir=''):
    '''
    QtWidgets.QFileDialog.getExistingDirectory が inspect.argspec に通らないので関数でラップ
    '''
    dir = QtWidgets.QFileDialog.getExistingDirectory(parent, dir=dir)
    return dir


class FilePathEdit(QtWidgets.QWidget):
    '''
    ファイルパス用ウィジェット
    '''

    filter = 'All files (*)'
    open_method = getOpenFileName
    textChanged = QtCore.Signal(str)
    editingFinished = QtCore.Signal()
    
    def __init__(self, *args, **kwargs):
        super(FilePathEdit, self).__init__(*args, **kwargs)
        hlo = QtWidgets.QHBoxLayout()
        hlo.setContentsMargins(0,0,0,0)
        hlo.setSpacing(0)
        self.setLayout(hlo)

        # LineEdit
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.textChanged.connect(self.textChanged)
        self.line_edit.editingFinished.connect(self.editingFinished)
        hlo.addWidget(self.line_edit)

        # Dialog Button
        self.dialog_btn = QtWidgets.QPushButton()
        self.dialog_btn.setStyleSheet('background-color: transparent; border-style: solid; border-width:0px;')
        self.dialog_btn.setIcon(dir_icon)
        self.dialog_btn.clicked.connect(self.open_dialog)
        hlo.addWidget(self.dialog_btn)

    def open_dialog(self):
        crr_path = self.text()
        crr_dir = os.path.dirname(crr_path) if os.path.isfile(crr_path) else crr_path
        kwargs = {
                'dir': crr_dir,
                'filter': self.filter,
                }
        argspec = inspect.getargspec(self.open_method)
        kwargs = {key: value for key, value in kwargs.items() if key in argspec.args}
        result = self.open_method(**kwargs)

        if result:
            self.setText(result)

        return result

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)

class DirectoryPathEdit(FilePathEdit):
    '''
    ディレクトリパス用ウィジェット
    '''
    open_method = getExistingDirectory

