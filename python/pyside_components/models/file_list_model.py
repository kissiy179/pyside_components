# -*- coding: utf-8 -*-
import os
import re
from qtpy import QtCore, QtGui, QtWidgets

class FileListModel(QtGui.QStandardItemModel):

    def __init__(self, root_dir_path='', file_paths=(), filters=(), parent=None):
        super(FileListModel, self).__init__(parent)

        if file_paths:
            self.__file_paths = file_paths

        elif root_dir_path:
            self.__file_paths = self.get_file_paths(root_dir_path)

        self.build_items(self.__file_paths, filters)

    def get_file_paths(self, root_dir_path):
        file_paths = []

        for dir_path, dir_names, file_names in os.walk(root_dir_path):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                file_paths.append(file_path)

        return file_paths

    def get_compiled_filters(self, filters=()):
        # フィルタを拡張子と通常のものに分離
        ext_filter_txts = [filter_ for filter_ in filters if filter_.startswith('.')]
        normal_filter_txts = [filter_ for filter_ in filters if not filter_.startswith('.')]
        ext_filter_pattern_txts = []
        normal_filter_pattern_txts = []

        # 拡張子の場合
        for filter_txt in ext_filter_txts:
            filter_pattern_txt = r'(?=.*\{}$)'.format(filter_txt)
            ext_filter_pattern_txts.append(filter_pattern_txt)

        ext_filters_pattern_txt = '|'.join(ext_filter_pattern_txts)

        # 通常の場合
        for filter_txt in normal_filter_txts:
            pattern_template = '(?=.*{})'

            if filter_txt.startswith('!'):
                filter_txt = filter_txt.strip('!')
                pattern_template = '(?!.*{})'

            filter_pattern_txt = pattern_template.format(filter_txt)
            normal_filter_pattern_txts.append(filter_pattern_txt)

        normal_filters_pattern_txt = ''.join(normal_filter_pattern_txts)

        #  パターンを結合
        filters_pattern_txt = '^({}){}.*$'.format(ext_filters_pattern_txt, normal_filters_pattern_txt)
        filters_pattern = re.compile(filters_pattern_txt)
        return filters_pattern

    def build_items(self, file_paths, filters=()):
        rootItem = self.invisibleRootItem()
        pattern = self.get_compiled_filters(filters)
        provider = QtWidgets.QFileIconProvider()

        for file_path in file_paths:
            m = pattern.match(file_path)

            if not m:
                continue

            icon = provider.icon(file_path)
            dir_path = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            dir_item = QtGui.QStandardItem(dir_path)
            file_item = QtGui.QStandardItem(file_name)
            file_item.setIcon(icon)
            rootItem.appendRow([file_item, dir_item])