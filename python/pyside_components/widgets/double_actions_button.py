# -*- coding: utf-8 -*-
from qtpy import QtCore, QtWidgets
import qtawesome as qta

removable_btn_style = '''
{class_name} {{
    padding: {padding_top}px {padding_right}px {padding_bottom}px {padding_left}px;
}}
'''

class DoubleActionsButtonMixin(object):

    def __init__(self, *args, **kwargs):
        super(DoubleActionsButtonMixin, self).__init__(*args, **kwargs)
        btn = self.add_inner_button()
        self.set_inner_button(btn)

    def add_inner_button(self):
        '''
        内部ボタンを追加
        オーバーライド前提
        '''
        btn = QtWidgets.QPushButton(parent=self)
        return btn

    def set_inner_button(self, btn):
        self.inner_btn = btn
        self.update_size()

    def update_size(self):
        '''
        内部ボタンのサイズを加味して自身のサイズを更新
        '''
        if not self.inner_btn:
            return

        btn_size = self.sizeHint()
        inner_btn_size = self.inner_btn.sizeHint()
        btn_height = btn_size.height()
        inner_btn_height = inner_btn_size.height()

        if btn_height > inner_btn_height:
            return

        height_sub = inner_btn_height - btn_height
        half_height_sub = height_sub // 2
        btn_margin, frame_width = self.get_pixcelmetric_info()
        padding = btn_margin - frame_width
        top_padding = padding if height_sub > 0 else padding -1
        self.setStyleSheet(removable_btn_style.format(class_name=type(self).__name__,
                                                      padding_top=half_height_sub + top_padding,
                                                      padding_right=inner_btn_size.width() + padding,
                                                      padding_bottom=half_height_sub + padding,
                                                      padding_left=padding))
        return

    def resizeEvent(self, event):
        if not self.inner_btn:
            return
            
        super(DoubleActionsButtonMixin, self).resizeEvent(event)
        inner_btn_size = self.inner_btn.sizeHint()
        _, frame_width = self.get_pixcelmetric_info()
        self.inner_btn.move(self.rect().right() + frame_width - inner_btn_size.width(),
                            self.rect().bottom() - inner_btn_size.height() + frame_width)

    def get_pixcelmetric_info(self):
        btn_margin = self.style().pixelMetric(QtWidgets.QStyle.PM_ButtonMargin)
        frame_width = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        return btn_margin, frame_width

class DoubleActionsButton(DoubleActionsButtonMixin, QtWidgets.QPushButton):

    def __init__(self, text='', parent=None):
        super(DoubleActionsButton, self).__init__(text, parent)
