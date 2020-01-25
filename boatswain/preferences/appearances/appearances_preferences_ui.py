#  This file is part of Boatswain.
#
#      Boatswain<https://github.com/theboatswain> is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Boatswain is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QScrollArea, QFrame, QWidget, QHBoxLayout, QLabel, \
    QPushButton

from boatswain.common.services import system_service
from boatswain.common.services.system_service import rt, applyFontRatio
from boatswain.common.ui.custom_ui import AutoResizeWidget, BQSizePolicy, BorderedButton
from boatswain.common.utils.app_avatar import AppAvatar
from boatswain.common.utils.utils import tr


class AppearancesPreferencesUi(AutoResizeWidget):

    def preferableSize(self) -> QSize:
        height = system_service.getRefHeight() / 2
        width = height * 1.8
        return QSize(width, height * 0.7)

    def __init__(self, parent, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(rt(20), rt(11), rt(20), rt(11))
        self.vertical_layout.setSpacing(rt(6))

        self.top_widget = QtWidgets.QWidget(self)
        self.top_widget.setSizePolicy(BQSizePolicy(v_stretch=2))

        self.scroll_area = QScrollArea(self.top_widget)
        self.scroll_area.verticalScrollBar().resize(0, 0)
        self.scroll_area.horizontalScrollBar().resize(0, 0)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)

        self.scroll_area.setStyleSheet('''QScrollArea { background: transparent; }
                QScrollArea > QWidget > QWidget { background: transparent; }
                QScrollArea > QWidget > QScrollBar { background: palette(base); }''')

        self.theme_list = QWidget(self.top_widget)
        self.theme_list.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.theme_list)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(0)
        self.horizontal_layout.setAlignment(Qt.AlignCenter)
        self.theme_list.setLayout(self.horizontal_layout)
        self.scroll_area.setWidget(self.theme_list)

        self.vertical_layout.addWidget(self.scroll_area)
        self.top_line = QtWidgets.QFrame(self)
        self.top_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.top_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_layout.addWidget(self.top_line)

        self.mid_widget = QtWidgets.QWidget(self)
        self.mid_widget.setSizePolicy(BQSizePolicy(v_stretch=2))
        self.gridLayout_2 = QtWidgets.QGridLayout(self.mid_widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(rt(6))
        self.background_label = QtWidgets.QLabel(self.mid_widget)
        self.background_label.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.gridLayout_2.addWidget(self.background_label, 0, 0, 1, 1)
        self.bg_color = BorderedButton(self.mid_widget)
        self.bg_color.setSizePolicy(BQSizePolicy(h_stretch=1, width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.bg_color.setFixedWidth(rt(70))
        self.gridLayout_2.addWidget(self.bg_color, 0, 1, 1, 1)
        self.hidden_widget = QtWidgets.QWidget(self.mid_widget)
        self.hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.gridLayout_2.addWidget(self.hidden_widget, 0, 3, 1, 1)

        self.font_label = QtWidgets.QLabel(self.mid_widget)
        self.gridLayout_2.addWidget(self.font_label, 1, 0, 1, 1)
        self.font_color = BorderedButton(self.mid_widget)
        self.font_color.setFixedWidth(rt(70))
        self.font_color.setSizePolicy(BQSizePolicy(h_stretch=1, width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.gridLayout_2.addWidget(self.font_color, 1, 1, 1, 1)

        self.selection_label = QtWidgets.QLabel(self.mid_widget)
        self.gridLayout_2.addWidget(self.selection_label, 2, 0, 1, 1)
        self.selection_color = BorderedButton(self.mid_widget)
        self.selection_color.setFixedWidth(rt(70))
        self.selection_color.setSizePolicy(BQSizePolicy(h_stretch=1, width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.gridLayout_2.addWidget(self.selection_color, 2, 1, 1, 1)

        self.hidden_widget_2 = QtWidgets.QWidget(self.mid_widget)
        self.hidden_widget_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.gridLayout_2.addWidget(self.hidden_widget_2, 0, 4, 1, 2)

        self.vertical_layout.addWidget(self.mid_widget)

        self.retranslateUi()

    def retranslateUi(self):
        self.background_label.setText(tr("Background color:"))
        self.font_label.setText(tr("Font color:"))
        self.selection_label.setText(tr("Selection color:"))

    def generateAppearanceUnit(self, parent, theme_name, definition: str):
        unit = QWidget(parent)
        vertical_layout = QVBoxLayout(unit)
        vertical_layout.setContentsMargins(rt(20), rt(11), rt(20), rt(11))
        vertical_layout.setSpacing(rt(6))
        vertical_layout.setAlignment(Qt.AlignCenter)
        visualise = QWidget(unit)
        visualise.setSizePolicy(BQSizePolicy(v_stretch=3))
        visualise.setFixedSize(QSize(rt(80), rt(50)))
        visualise.setProperty('class', 'home')
        visualise.setStyleSheet("QWidget.home { border-radius: 8px; }")

        app_widget_layout = QVBoxLayout(visualise)
        app_widget_layout.setContentsMargins(0, 12, 0, 10)
        app_widget_layout.setSpacing(0)

        line = QFrame(visualise)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        app_widget_layout.addWidget(line)

        widget = QWidget(visualise)
        widget.setProperty('class', 'app-widget')
        app_widget_layout.addWidget(widget)
        app_horizontal_layout = QHBoxLayout(widget)
        app_horizontal_layout.setContentsMargins(rt(4), 0, rt(4), 0)
        app_horizontal_layout.setSpacing(2)
        pic = AppAvatar(None, "Sample", parent=widget, radius=rt(5), font_size=applyFontRatio(7))
        app_horizontal_layout.addWidget(pic)

        font = QFont()
        font.setPointSize(applyFontRatio(2))

        name = QLabel(widget)
        name.setFont(font)
        name.setText("Sample application")
        name.setSizePolicy(BQSizePolicy(h_stretch=2))
        app_horizontal_layout.addWidget(name)

        status = QPushButton(widget)
        status.setFlat(True)
        status.setFont(font)
        status.setProperty('class', 'bordered-widget')
        status.setStyleSheet('padding: 0 %dpx' % rt(1))
        app_horizontal_layout.addWidget(status)

        line = QFrame(visualise)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        app_widget_layout.addWidget(line)

        vertical_layout.addWidget(visualise)

        label = QtWidgets.QLabel(unit)
        label.setText(theme_name)
        label.setAlignment(Qt.AlignCenter)
        vertical_layout.addWidget(label)
        unit.setStyleSheet(definition)

        return unit
