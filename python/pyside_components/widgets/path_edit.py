# -*- coding: utf-8 -*-
import os
import inspect
from re import S
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
    current_dir = ''
    
    def __init__(self, *args, **kwargs):
        super(FilePathEdit, self).__init__(*args, **kwargs)
        hlo = QtWidgets.QHBoxLayout()
        hlo.setContentsMargins(0,0,0,0)
        hlo.setSpacing(0)
        self.setLayout(hlo)

        # LineEdit
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.line_edit.setClearButtonEnabled(True)
        self.line_edit.textChanged.connect(self.textChanged)
        self.line_edit.editingFinished.connect(self.editingFinished)
        self.line_edit.textChanged.connect(self.set_stylesheet)
        hlo.addWidget(self.line_edit)

        # Dialog Button
        self.dialog_btn = QtWidgets.QPushButton()
        self.dialog_btn.setIcon(dir_icon)
        self.dialog_btn.clicked.connect(self.open_dialog)
        hlo.addWidget(self.dialog_btn)

        # stylesheet
        self.set_stylesheet()
        
    def open_dialog(self):
        text = self.text()
        crr_path = text if os.path.exists(text) else self.current_dir
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
        self.editingFinished.emit()

    def set_stylesheet(self):
        stylesheets = {}
        text = self.text()

        # LineEdit
        line_edit_style = ''

        if not os.path.exists(text):
            line_edit_style += 'color: indianred;'

        self.line_edit.setStyleSheet(line_edit_style)
        stylesheets[self.line_edit] = line_edit_style

        # Diaglog button
        dialog_btn_style = 'background-color: transparent; border-style: solid; border-width:0px;'
        self.dialog_btn.setStyleSheet(dialog_btn_style)
        stylesheets[self.dialog_btn] = dialog_btn_style
        return stylesheets


class DirectoryPathEdit(FilePathEdit):
    '''
    ディレクトリパス用ウィジェット
    '''
    open_method = getExistingDirectory

