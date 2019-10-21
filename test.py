# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/manhtu/Downloads/test/test-project/untitled/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(573, 166)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setMinimumSize(QtCore.QSize(335, 166))
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.changes = QtWidgets.QWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.changes.sizePolicy().hasHeightForWidth())
        self.changes.setSizePolicy(sizePolicy)
        self.changes.setObjectName("changes")
        self.verticalLayout.addWidget(self.changes)
        self.toolbox = QtWidgets.QWidget(self.centralWidget)
        self.toolbox.setObjectName("toolbox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.toolbox)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel = QtWidgets.QPushButton(self.toolbox)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.hidden = QtWidgets.QWidget(self.toolbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hidden.sizePolicy().hasHeightForWidth())
        self.hidden.setSizePolicy(sizePolicy)
        self.hidden.setObjectName("hidden")
        self.horizontalLayout.addWidget(self.hidden)
        self.old_conf = QtWidgets.QPushButton(self.toolbox)
        self.old_conf.setObjectName("old_conf")
        self.horizontalLayout.addWidget(self.old_conf)
        self.merge = QtWidgets.QPushButton(self.toolbox)
        self.merge.setObjectName("merge")
        self.horizontalLayout.addWidget(self.merge)
        self.verticalLayout.addWidget(self.toolbox)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "There are some changed configurations that required the container to be reset. Please consider using Volume Mapping to preserve your data."))
        self.label_2.setText(_translate("MainWindow", "Click here to see those changed configurations."))
        self.cancel.setText(_translate("MainWindow", "Cancel"))
        self.old_conf.setToolTip(_translate("MainWindow", "Launch the application with the old configurations"))
        self.old_conf.setText(_translate("MainWindow", "Use the old configuations"))
        self.merge.setToolTip(_translate("MainWindow", "Merge the old with the new configurations and launch the application"))
        self.merge.setText(_translate("MainWindow", "Merge"))
