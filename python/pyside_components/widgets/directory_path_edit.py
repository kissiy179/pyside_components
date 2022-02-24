# -*- coding: utf-8 -*-
import os
import inspect
from qtpy import QtWidgets, QtCore
import qtawesome as qta
from . file_path_edit import FilePathEdit

def getExistingDirectory(parent, dir=''):
    '''
    QtWidgets.QFileDialog.getExistingDirectory が inspect.argspec に通らないので関数でラップ
    '''
    dir = QtWidgets.QFileDialog.getExistingDirectory(parent, dir=dir)
    return dir

class DirectoryPathEdit(FilePathEdit):
    '''
    ディレクトリパス用ウィジェット
    '''
    open_method = getExistingDirectory

