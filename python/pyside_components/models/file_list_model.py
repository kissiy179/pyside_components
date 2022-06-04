# -*- coding: utf-8 -*-
import os
import re
from qtpy import QtCore, QtGui, QtWidgets
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.schema import Column, Table, MetaData
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, select, and_, or_, not_

# from sqlalchemy_views import CreateView, DropView
Base = declarative_base()
echo = False
icon_provider = QtWidgets.QFileIconProvider()

class ProgressBar(QtWidgets.QProgressBar):
    '''
    プログレスバー
    '''

    __idx = 0
    app = QtWidgets.QApplication

    def __init__(self, maximum, parent=None):
        super(ProgressBar, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle('Search files...')
        self.setMaximum(maximum)
        # self.move(QtGui.QCursor().pos())

    def increment(self):
        self.__idx += 1
        self.setValue(self.__idx)
        self.app.processEvents()

        if self.__idx > self.maximum():
            self.close()

class FileInfo(Base):
    '''
    ファイルパスを格納するテーブル
    '''
    __tablename__ = "file_infos"  # テーブル名を指定
    id = Column(Integer, primary_key=True)
    file_path = Column(String(255))
    extention = Column(String(255))

class FileListDB(object):
    '''
    ルートディレクトリ以下のすべてのファイルパスを扱うDBクラス
    DBから取得したデータはget_resultで取り出す
    '''
    __root_dir_path = ''
    __filters = []
    __result = []
    __engine = None
    __session = None

    def __init__(self, root_dir_path='', filters=()):
        super(FileListDB, self).__init__()
        self.set_root_path(root_dir_path)
        self.set_filters(filters)

    def get_root_path(self):
        return self.__root_dir_path

    def set_root_path(self, root_dir_path):
        '''
        ルートディレクトリパスを指定する
        パス指定と同時にDBビルドする
        '''
        root_dir_path = root_dir_path.replace(os.altsep, os.sep)
        self.__root_dir_path = root_dir_path
        self.build(self.__root_dir_path)
        
    def get_filters(self):
        return self.__filters

    def set_filters(self, filters):
        '''
        フィルタを設定する
        DBにフィルタを適用してresultを更新する
        '''
        self.__filters = filters
        self.filter(self.__filters)

    def get_result(self):
        '''
        DBから取得した結果を取得する
        '''
        return self.__result

    def build(self, root_dir_path):
        '''
        DBをビルドする
        ルートディレクトリ以下のすべてのファイルを登録する
        '''
        self.__engine = create_engine('sqlite:///:memory:', echo=echo)
        Base.metadata.create_all(self.__engine)
        SessionClass = sessionmaker(bind=self.__engine)
        self.__session = SessionClass()
        file_paths = []

        for dir_path, dir_names, file_names in os.walk(root_dir_path):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                file_paths.append(file_path)

        prog = ProgressBar(len(file_paths))
        prog.show()

        for i, file_path in enumerate(file_paths):
            file_path_, ext = os.path.splitext(file_path)
            file_info = FileInfo(
                file_path = file_path,
                extention = ext,
            )
            prog.increment()

            try:
                self.__session.add(file_info)

            except Exception as e:
                print(e)

        self.__session.commit()
        self.__reuslt = file_paths

    def filter(self, filters=()):
        '''
        DBにフィルタを適用してresultを更新する
        '''
        # 拡張子用/通常テキスト用フィルタ関数リスト
        ext_filters = []
        normal_filters = []

        # フィルタ文字列からフィルタ関数を作成しリストに登録
        for filter_ in filters:
            is_not = False
            target_filters = normal_filters

            # 「!」で始まる場合否定として扱う
            if filter_.startswith('!'):
                is_not = True
                filter_ = filter_.strip('!') # 「!」を除外

            # 「.」で始まる場合拡張子用
            if filter_.startswith('.'):
                filter_fiunc = FileInfo.extention.like('%{}'.format(filter_))
                target_filters = ext_filters

            else:
                filter_fiunc = FileInfo.file_path.like('%{}%'.format(filter_))

            # 関数の否定化
            if is_not:
                filter_fiunc = not_(filter_fiunc)
                
            # リストに登録
            target_filters.append(filter_fiunc)

        # SQLに問い合わせ
        query = self.__session.query(FileInfo).filter(
            and_(*normal_filters),
            or_(*ext_filters)
        ).yield_per(10)

        self.__result = [row.file_path for row in query]

class FileItem(object):
    '''
    ファイルアイテムを扱うクラス
    '''
    # ヘッダーリスト
    __headers = ['Idx', 'File Name', 'Directory Path', 'Extension']

    # {ヘッダー: インデックス} という形式のdict
    __header_idx_table = {value: idx for idx, value in enumerate(__headers)}

    def __init__(self, path):
        self.__path = path
        self.__dir_path = os.path.dirname(self.__path)
        self.__name = os.path.basename(self.__path)

    @property
    def path(self):
        return self.__path

    def data(self, index, role):
        row = index.row()
        column = index.column()

        # 表示文字
        if role == QtCore.Qt.DisplayRole:
            if column == self.__header_idx_table.get('Idx'):
                return row

            elif column == self.__header_idx_table.get('File Name'):
                return self.__name

            elif column == self.__header_idx_table.get('Directory Path'):
                return self.__dir_path

            elif column == self.__header_idx_table.get('Extension'):
                return os.path.splitext(self.__name)[-1]

        # 背景色
        elif role == QtCore.Qt.BackgroundRole:
            if row % 2:
                return QtGui.QColor('#333')

            else:
                return QtGui.QColor('#3a3a3a')

        # アイコン
        elif role == QtCore.Qt.DecorationRole:
            if column == self.__headers.index('File Name'):
                return icon_provider.icon(self.__path)

        # 行のサイズ
        # elif role == QtCore.Qt.SizeHintRole:
        #     return QtCore.QSize(28, 28)
                
    @classmethod
    def columnCount(cls):
        return len(cls.__headers)

    @classmethod
    def headerData(cls, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return cls.__headers[section]

        else:
            if role == QtCore.Qt.DisplayRole:
                return section

        return None

class DummyItem(object):
    
    def __init__(self, path):
        self.path = path

    @classmethod
    def columnCount(cls):
        return 3

    def data(self, index, role):
        col = index.column()

        if role == QtCore.Qt.DisplayRole:
            if col == 0:
                return self.path

            else:
                return self.__class__.__name__

        elif role == QtCore.Qt.ForegroundRole:
            return QtGui.QColor('red')

        elif role == QtCore.Qt.BackgroundRole:
            return QtGui.QColor('yellow')

        elif role == QtCore.Qt.DecorationRole:
            if col == 0:
                return icon_provider.icon(self.path)

class FileListModel(QtCore.QAbstractItemModel):
    '''
    ファイルリストを扱うモデル
    多くのメソッドは__item_classで指定したクラスに移譲する
    '''
    __db = None
    # __item_class = FileItem
    __items = []

    def __init__(self, root_dir_path='', filters=(), item_class=FileItem, parent=None):
        super(FileListModel, self).__init__(parent)
        self.__db = FileListDB(root_dir_path, filters)
        self.__item_class = item_class
        self.build()

    def __getattr__(self, attrname):
        '''
        アトリビュートが見つからない場合DBクラスの同名アトリビュートを取得
        '''
        attr = getattr(self.__db, attrname)
        return attr

    def build(self):
        '''
        DBを値を取り出しresultを更新
        '''
        del self.__items[:]
        file_paths =self.__db.get_result()

        for file_path in file_paths:
            self.__items.append(self.__item_class(file_path))

        # モデルがリセットされていることを通知する
        self.modelReset.emit()

    def set_root_path(self, root_dir_path):
        '''
        DBにルートディレクトリを設定し、自身をビルド
        '''
        self.__db.set_root_path(root_dir_path)
        self.build()

    def set_filters(self, filters):
        '''
        DBにフィルタを設定し、自身をビルド
        '''
        self.__db.set_filters(filters)
        self.build()

    def columnCount(self, parent=None):
        if hasattr(self.__item_class, 'columnCount'):
            return self.__item_class.columnCount()

        return 1

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.__items)

        return 0

    def parent(self, index):
        return QtCore.QModelIndex()

    def index(self, row, column, parent):
        if parent.isValid():
            return QtCore.QModelIndex()

        item = self.__items[row]
        return self.createIndex(row, column, item)

    def data(self, index, role):
        if not index.isValid():
            return

        item = index.internalPointer()

        if hasattr(item, 'data'):
            return item.data(index, role)

        if role == QtCore.Qt.DisplayRole:
            return 'data'

    def headerData(self, section, orientation, role):
        if hasattr(self.__item_class, 'headerData'):
            return self.__item_class.headerData(section, orientation, role)

        return super(FileListModel, self).headerData(section, orientation, role)

