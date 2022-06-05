# -*- coding: utf-8 -*-
from functools import partial
from pprint import pprint
from qtpy import QtCore, QtWidgets
import qtawesome as qta
from .tag_item_button import TagItemButton
from ..layouts.flow_layout import FlowLayout
from .temporary_line_edit import TemporaryLineEdit

lineedit_style = '''
QLineEdit {
    border-radius: 3px;
}
'''

class LineEditForAddingTag(TemporaryLineEdit):

    def __init__(self, parent=None):
        super(LineEditForAddingTag, self).__init__(parent)
        self.setMinimumSize(100, 23)
        self.setStyleSheet(lineedit_style)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setPlaceholderText('Add tag...')

        try:
            self.setClearButtonEnabled(True)

        except:
            pass

class TagEdit(QtWidgets.QWidget):
    '''
    複数タグを扱うウィジェット
    タグの追加、削除、ON/OFFが可能

    タグ情報は以下のフォーマットの辞書に格納する
    {
        <タグ名>: <有効かどうか>,
        <タグ名>: <有効かどうか>,
        ...
    }
    '''

    __tag_infos = {}
    updated = QtCore.Signal()

    def __init__(self, tags={}, parent=None):
        '''
        初期化
        '''
        super(TagEdit, self).__init__(parent)
        self.__tag_infos = tags
        self.init_ui()

    def clear_ui(self):
        '''
        UIクリア
        '''
        dmy_wgt = QtWidgets.QWidget()
        dmy_wgt.setLayout(self.layout())
        del dmy_wgt

    def init_ui(self):
        '''
        UI初期化
        '''
        self.clear_ui()
        self.lo = FlowLayout(vspacing=3, hspacing=3)
        self.lo.setContentsMargins(0,0,0,0)
        # self.lo.setSpacing(5)
        self.setLayout(self.lo)
        tags = self.__tag_infos

        # LineEdit
        self.line_edit = LineEditForAddingTag()
        self.line_edit.editingFinished.connect(self.add_tag2)
        self.lo.addWidget(self.line_edit)

        for tag_name, enabled in sorted(tags.items()):
            btn = TagItemButton(tag_name, self)
            btn.setObjectName(tag_name)
            btn.setChecked(enabled)
            btn.toggled.connect(partial(self.set_tag_enabled, tag_name))
            btn.closed.connect(partial(self.remove_tag, tag_name))
            # btn.text_changed.connect(partial(self.change_tag, tag_name))
            self.lo.addWidget(btn)#, QtCore.Qt.AlignLeft)
            # self.__buttons.append(btn)

    def add_tag(self, tag_name):
        '''
        タグを追加
        '''
        if not isinstance(tag_name, basestring) or not tag_name:
            return

        self.__tag_infos[tag_name] = True
        self.init_ui()
        self.updated.emit()

    def add_tag2(self):
        tag = self.line_edit.text()
        self.add_tag(tag)

    def remove_tag(self, tag_name):
        '''
        タグを削除
        '''
        if not tag_name in self.__tag_infos:
            return
            
        del self.__tag_infos[tag_name]
        self.updated.emit()
        
    def set_tag_enabled(self, tag_name, enabled):
        '''
        タグが有効化どうかを設定する
        '''
        if not tag_name in self.__tag_infos.keys():
            return
            
        self.__tag_infos[tag_name] = enabled
        self.updated.emit()

    def change_tag(self, old_tag_name, new_tag_name):
        '''
        タグ名を変更する
        '''
        if not old_tag_name in self.__tag_infos or new_tag_name in self.__tag_infos:
            return

        enabled = self.__tag_infos.get(old_tag_name, True)
        del self.__tag_infos[old_tag_name]
        self.__tag_infos[new_tag_name] = enabled
        self.updated.emit()

    def get_tag_infos(self):
        '''
        タグ情報を取得
        '''
        return self.__tag_infos

    def set_tag_infos(self, tags):
        '''
        タグ情報を設定
        '''
        self.__tag_infos = tags
        self.init_ui()
        self.updated.emit()

    def get_enabled_tag_names(self):
        '''
        有効なタグ名を取得
        '''
        tag_names = [tag for tag, enabled in self.__tag_infos.items() if enabled]
        return sorted(tag_names)

    def show_tags(self):
        '''
        タグを表示
        '''
        tags = self.get_enabled_tag_names()
        print(tags)

    

'''
import pyside_components; reload(pyside_components)
from pyside_components.widgets.tag_edit import TagEdit

tag_edit = TagEdit()
tag_edit.set_tag_infos({'animations': True, 'characters': False, 'rig': True})
tag_edit.show()
'''