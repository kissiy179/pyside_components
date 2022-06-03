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
        root_dir_path = root_dir_path.replace(os.altsep, os.sep)
        self.__root_dir_path = root_dir_path
        self.build(self.__root_dir_path)
        
    def get_filters(self):
        return self.__filters

    def set_filters(self, filters):
        self.__filters = filters
        self.filter(self.__filters)

    def get_result(self):
        return self.__result

    def build(self, root_dir_path):
        # if self.__session:
        #     self.__session.close()
            # self.__session.dispose()

        self.__engine = create_engine('sqlite:///:memory:', echo=echo)
        Base.metadata.create_all(self.__engine)
        SessionClass = sessionmaker(bind=self.__engine)
        self.__session = SessionClass()

        file_paths = []

        for dir_path, dir_names, file_names in os.walk(root_dir_path):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)

                file_paths.append(file_path)

        app = QtWidgets.QApplication
        prog = QtWidgets.QProgressDialog('Search files...', None, 0, len(file_paths), None, 0)
        prog.setWindowFlags(QtCore.Qt.Popup)
        prog.show()

        for i, file_path in enumerate(file_paths):
            file_path_, ext = os.path.splitext(file_path)
            file_info = FileInfo(
                file_path = file_path,
                extention = ext,
            )
            prog.setValue(i)
            app.processEvents()

            try:
                self.__session.add(file_info)

            except Exception as e:
                print(e)

        self.__session.commit()
        # self.__session.close()

    def filter(self, filters=()):
        ext_filters = []
        normal_filters = []

        for f in filters:
            if f.startswith('!'):
                f = f.strip('!')

                if f.startswith('.'):
                    f_ = not_(FileInfo.extention.like('%{}'.format(f)))
                    ext_filters.append(f_)

                else:
                    f_ = not_(FileInfo.file_path.like('%{}%'.format(f)))
                    normal_filters.append(f_)
            else:
                if f.startswith('.'):
                    f_ = FileInfo.extention.like('%{}'.format(f))
                    ext_filters.append(f_)

                else:
                    f_ = FileInfo.file_path.like('%{}%'.format(f))
                    normal_filters.append(f_)

        # SessionClass = sessionmaker(bind=self.__engine)
        # self.__session = SessionClass()
        query = self.__session.query(FileInfo).filter(
            and_(*normal_filters),
            or_(*ext_filters)
        ).all()

        self.__result = [row.file_path for row in query]
        # self.__session.commit()
        # self.__session.close()

# class FileListModel(QtGui.QStandardItemModel):
class FileListModel(QtGui.QStringListModel):

    __root_dir_path = ''
    __filters = []
    __engine = None
    __db = None

    def __init__(self, root_dir_path='', filters=(), parent=None):
        super(FileListModel, self).__init__(parent)
        self.__db = FileListDB(root_dir_path, filters)
        file_paths = self.__db.get_result()
        self.setStringList(file_paths)

    def __getattr__(self, attrname):
        attr = getattr(self.__db, attrname)
        return attr

    def set_filters(self, filters):
        self.__db.set_filters(filters)
        file_paths = self.__db.get_result()
        self.setStringList(file_paths)
