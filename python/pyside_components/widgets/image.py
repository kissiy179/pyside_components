# -*- coding: utf-8 -*-
import os
from functools import partial
from qtpy import QtCore, QtGui, QtWidgets
import qtawesome as qta

OPTION_ICON = qta.icon('fa5s.ellipsis-v', color='lightgray')

class Image(QtWidgets.QLabel):

    def __init__(self, path='', scale=1.0, use_option_menu=False, parent=None):
        super(Image, self).__init__(parent)
        self.__path = path
        self.__scale = scale
        self.__use_option_menu = use_option_menu
        self.init_ui()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

    def init_ui(self):
        # 画像表示
        if not os.path.exists(self.__path):
            return

        self.pixmap = QtGui.QPixmap(self.__path)

        if self.scale != 1.0:
            w = self.pixmap.width() * self.__scale
            h = self.pixmap.height() * self.__scale
            self.pixmap = self.pixmap.scaled(w, h)
            
        self.setPixmap(self.pixmap)

        # オプションメニュー
        if self.__use_option_menu:
            # レイアウト
            vlo = QtWidgets.QVBoxLayout()
            # vlo.setContentsMargins(0,0,0,0)
            self.setLayout(vlo)
            hlo = QtWidgets.QHBoxLayout()
            hlo.setContentsMargins(0,0,0,0)
            hlo.addStretch()
            vlo.addLayout(hlo, align=QtCore.Qt.AlignTop)
            vlo.addStretch()

            # オプションボタン
            option_btn = QtWidgets.QPushButton()
            option_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            option_btn.setIcon(OPTION_ICON)
            option_btn.setStyleSheet('* {background-color: transparent; border-style: solid;} ')
            option_btn.clicked.connect(self.open_menu)
            hlo.addWidget(option_btn)

            # メニュー
            self.init_actions()
            self.init_menu()

    def init_actions(self):
        # スケールアクション
        self.scale_25_action = QtWidgets.QAction('x 0.25', self)
        self.scale_25_action.triggered.connect(partial(self.scale, 0.25))
        self.scale_50_action = QtWidgets.QAction('x 0.5', self)
        self.scale_50_action.triggered.connect(partial(self.scale, 0.5))
        self.scale_75_action = QtWidgets.QAction('x 0.75', self)
        self.scale_75_action.triggered.connect(partial(self.scale, 0.75))
        self.scale_100_action = QtWidgets.QAction('x 1', self)
        self.scale_100_action.triggered.connect(partial(self.scale, 1))


    def init_menu(self):
        self.menu = QtWidgets.QMenu()
        self.menu.addAction(self.scale_25_action)
        self.menu.addAction(self.scale_50_action)
        self.menu.addAction(self.scale_75_action)
        self.menu.addAction(self.scale_100_action)

    def open_menu(self):
        self.menu.exec_(QtGui.QCursor.pos())

    def set_path(self, path):
        self.__path = path
        self.init_ui()

    def scale(self, scale):
        self.__scale = scale
        self.init_ui()

