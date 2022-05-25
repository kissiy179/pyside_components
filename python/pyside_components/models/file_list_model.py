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

class FileInfo(Base):
    '''
    ファイルパスを格納するテーブル
    '''
    __tablename__ = "file_infos"  # テーブル名を指定
    id = Column(Integer, primary_key=True)
    file_path = Column(String(255))
    extention = Column(String(255))

class FileListModel(QtGui.QStandardItemModel):

    __root_dir_path = ''
    __file_paths = []
    __filters = []
    __compiled_filter = None
    __engine = None

    def __init__(self, root_dir_path='', filters=(), parent=None):
        super(FileListModel, self).__init__(parent)
        self.set_root_path(root_dir_path)
        self.set_filters(filters)

    def set_root_path(self, root_dir_path):
        self.__root_dir_path = root_dir_path
        self.build_data(self.__root_dir_path)

    def set_filters(self, filters):
        self.__filters = filters
        self.filter(self.__filters)

    def build_data(self, root_dir_path):
        self.__engine = create_engine('sqlite:///:memory:')#, echo=True)
        Base.metadata.create_all(self.__engine)
        SessionClass = sessionmaker(bind=self.__engine)
        session = SessionClass()

        for dir_path, dir_names, file_names in os.walk(root_dir_path):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                file_path_, ext = os.path.splitext(file_path)
                file_info = FileInfo(
                    file_path = file_path,
                    extention = ext,
                )

                try:
                    session.add(file_info)

                except Exception as e:
                    print(e)

        session.commit()
        session.close()
        print('end build')

    def filter(self, filters=()):
        self.clear()
        ext_filters = [FileInfo.extention.like('%{}'.format(f)) for f in filters if f.startswith('.')]
        normal_filters = [FileInfo.file_path.like('%{}%'.format(f)) for f in filters if not f.startswith('.')]
        SessionClass = sessionmaker(bind=self.__engine)
        session = SessionClass()
        query = session.query(FileInfo).filter(
            and_(*normal_filters),
            or_(*ext_filters)
        ).all()

        root_item = self.invisibleRootItem()
        provider = QtWidgets.QFileIconProvider()
        
        for row in query:
            file_path = row.file_path
            icon = provider.icon(file_path)
            dir_path = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            dir_item = QtGui.QStandardItem(dir_path)
            file_item = QtGui.QStandardItem(file_name)
            file_item.setIcon(icon)
            root_item.appendRow([file_item, dir_item])

        session.commit()
        session.close()
        print('end filters', filters)