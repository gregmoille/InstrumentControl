# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dw_widgets.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(269, 306)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_81 = QtGui.QLabel(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_81.setFont(font)
        self.label_81.setObjectName(_fromUtf8("label_81"))
        self.gridLayout.addWidget(self.label_81, 0, 1, 1, 1)
        self.label_82 = QtGui.QLabel(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_82.setFont(font)
        self.label_82.setObjectName(_fromUtf8("label_82"))
        self.gridLayout.addWidget(self.label_82, 0, 2, 1, 1)
        self.label_56 = QtGui.QLabel(self.dockWidgetContents)
        self.label_56.setMinimumSize(QtCore.QSize(0, 0))
        self.label_56.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_56.setFont(font)
        self.label_56.setObjectName(_fromUtf8("label_56"))
        self.gridLayout.addWidget(self.label_56, 1, 0, 1, 1)
        self.listWidget = QtGui.QListWidget(self.dockWidgetContents)
        self.listWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 1, 1, 1, 1)
        self.listWidgetDis = QtGui.QListWidget(self.dockWidgetContents)
        self.listWidgetDis.setEnabled(False)
        self.listWidgetDis.setObjectName(_fromUtf8("listWidgetDis"))
        item = QtGui.QListWidgetItem()
        self.listWidgetDis.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidgetDis.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidgetDis.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidgetDis.addItem(item)
        self.gridLayout.addWidget(self.listWidgetDis, 1, 2, 1, 1)
        self.label_57 = QtGui.QLabel(self.dockWidgetContents)
        self.label_57.setMinimumSize(QtCore.QSize(0, 0))
        self.label_57.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_57.setFont(font)
        self.label_57.setObjectName(_fromUtf8("label_57"))
        self.gridLayout.addWidget(self.label_57, 2, 0, 1, 1)
        self.treeWidget = QtGui.QTreeWidget(self.dockWidgetContents)
        self.treeWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.treeWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.gridLayout.addWidget(self.treeWidget, 2, 1, 1, 1)
        self.treeWidgetDis = QtGui.QTreeWidget(self.dockWidgetContents)
        self.treeWidgetDis.setEnabled(False)
        self.treeWidgetDis.setObjectName(_fromUtf8("treeWidgetDis"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidgetDis)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidgetDis)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.gridLayout.addWidget(self.treeWidgetDis, 2, 2, 1, 1)
        self.label_58 = QtGui.QLabel(self.dockWidgetContents)
        self.label_58.setMinimumSize(QtCore.QSize(0, 0))
        self.label_58.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_58.setFont(font)
        self.label_58.setObjectName(_fromUtf8("label_58"))
        self.gridLayout.addWidget(self.label_58, 3, 0, 1, 1)
        self.tableWidget = QtGui.QTableWidget(self.dockWidgetContents)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(3)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(1, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(2, 1, item)
        self.gridLayout.addWidget(self.tableWidget, 3, 1, 1, 1)
        self.tableWidgetDis = QtGui.QTableWidget(self.dockWidgetContents)
        self.tableWidgetDis.setEnabled(False)
        self.tableWidgetDis.setObjectName(_fromUtf8("tableWidgetDis"))
        self.tableWidgetDis.setColumnCount(2)
        self.tableWidgetDis.setRowCount(3)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setItem(1, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setItem(2, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDis.setItem(2, 1, item)
        self.gridLayout.addWidget(self.tableWidgetDis, 3, 2, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "Widgets", None))
        self.label_81.setText(_translate("DockWidget", "Enabled", None))
        self.label_82.setText(_translate("DockWidget", "Disabled", None))
        self.label_56.setToolTip(_translate("DockWidget", "This is a tool tip", None))
        self.label_56.setStatusTip(_translate("DockWidget", "This is a status tip", None))
        self.label_56.setWhatsThis(_translate("DockWidget", "This is \"what is this\"", None))
        self.label_56.setText(_translate("DockWidget", "ListWidget", None))
        self.listWidget.setToolTip(_translate("DockWidget", "This is a tool tip", None))
        self.listWidget.setStatusTip(_translate("DockWidget", "This is a status tip", None))
        self.listWidget.setWhatsThis(_translate("DockWidget", "This is \"what is this\"", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("DockWidget", "New Item", None))
        item = self.listWidget.item(1)
        item.setText(_translate("DockWidget", "New Item", None))
        item = self.listWidget.item(2)
        item.setText(_translate("DockWidget", "New Item", None))
        item = self.listWidget.item(3)
        item.setText(_translate("DockWidget", "New Item", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.listWidgetDis.isSortingEnabled()
        self.listWidgetDis.setSortingEnabled(False)
        item = self.listWidgetDis.item(0)
        item.setText(_translate("DockWidget", "New Item", None))
        item = self.listWidgetDis.item(1)
        item.setText(_translate("DockWidget", "New Item", None))
        item = self.listWidgetDis.item(2)
        item.setText(_translate("DockWidget", "New Item", None))
        item = self.listWidgetDis.item(3)
        item.setText(_translate("DockWidget", "New Item", None))
        self.listWidgetDis.setSortingEnabled(__sortingEnabled)
        self.label_57.setToolTip(_translate("DockWidget", "This is a tool tip", None))
        self.label_57.setStatusTip(_translate("DockWidget", "This is a status tip", None))
        self.label_57.setWhatsThis(_translate("DockWidget", "This is \"what is this\"", None))
        self.label_57.setText(_translate("DockWidget", "TreeWidget", None))
        self.treeWidget.setToolTip(_translate("DockWidget", "This is a tool tip", None))
        self.treeWidget.setStatusTip(_translate("DockWidget", "This is a status tip", None))
        self.treeWidget.setWhatsThis(_translate("DockWidget", "This is \"what is this\"", None))
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.headerItem().setText(0, _translate("DockWidget", "New Column", None))
        self.treeWidget.headerItem().setText(1, _translate("DockWidget", "New Column", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("DockWidget", "New Item", None))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("DockWidget", "New Subitem", None))
        self.treeWidget.topLevelItem(0).child(0).setText(1, _translate("DockWidget", "Test", None))
        self.treeWidget.topLevelItem(0).child(0).child(0).setText(0, _translate("DockWidget", "New Subitem", None))
        self.treeWidget.topLevelItem(1).setText(0, _translate("DockWidget", "New Item", None))
        self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("DockWidget", "New Subitem", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.treeWidgetDis.setSortingEnabled(True)
        self.treeWidgetDis.headerItem().setText(0, _translate("DockWidget", "New Column", None))
        self.treeWidgetDis.headerItem().setText(1, _translate("DockWidget", "New Column", None))
        __sortingEnabled = self.treeWidgetDis.isSortingEnabled()
        self.treeWidgetDis.setSortingEnabled(False)
        self.treeWidgetDis.topLevelItem(0).setText(0, _translate("DockWidget", "New Item", None))
        self.treeWidgetDis.topLevelItem(0).child(0).setText(0, _translate("DockWidget", "New Subitem", None))
        self.treeWidgetDis.topLevelItem(0).child(0).setText(1, _translate("DockWidget", "Test", None))
        self.treeWidgetDis.topLevelItem(0).child(0).child(0).setText(0, _translate("DockWidget", "New Subitem", None))
        self.treeWidgetDis.topLevelItem(1).setText(0, _translate("DockWidget", "New Item", None))
        self.treeWidgetDis.topLevelItem(1).child(0).setText(0, _translate("DockWidget", "New Subitem", None))
        self.treeWidgetDis.setSortingEnabled(__sortingEnabled)
        self.label_58.setToolTip(_translate("DockWidget", "This is a tool tip", None))
        self.label_58.setStatusTip(_translate("DockWidget", "This is a status tip", None))
        self.label_58.setWhatsThis(_translate("DockWidget", "This is \"what is this\"", None))
        self.label_58.setText(_translate("DockWidget", "TableWidget", None))
        self.tableWidget.setToolTip(_translate("DockWidget", "This is a tool tip", None))
        self.tableWidget.setStatusTip(_translate("DockWidget", "This is a status tip", None))
        self.tableWidget.setWhatsThis(_translate("DockWidget", "This is \"what is this\"", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("DockWidget", "New Row", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("DockWidget", "New Row", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("DockWidget", "New Row", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("DockWidget", "New Column", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("DockWidget", "New Column", None))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("DockWidget", "1.23", None))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("DockWidget", "Hello", None))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("DockWidget", "1,45", None))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("DockWidget", "Olá", None))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("DockWidget", "12/12/2012", None))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("DockWidget", "Oui", None))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        item = self.tableWidgetDis.verticalHeaderItem(0)
        item.setText(_translate("DockWidget", "New Row", None))
        item = self.tableWidgetDis.verticalHeaderItem(1)
        item.setText(_translate("DockWidget", "New Row", None))
        item = self.tableWidgetDis.verticalHeaderItem(2)
        item.setText(_translate("DockWidget", "New Row", None))
        item = self.tableWidgetDis.horizontalHeaderItem(0)
        item.setText(_translate("DockWidget", "New Column", None))
        item = self.tableWidgetDis.horizontalHeaderItem(1)
        item.setText(_translate("DockWidget", "New Column", None))
        __sortingEnabled = self.tableWidgetDis.isSortingEnabled()
        self.tableWidgetDis.setSortingEnabled(False)
        item = self.tableWidgetDis.item(0, 0)
        item.setText(_translate("DockWidget", "1.23", None))
        item = self.tableWidgetDis.item(0, 1)
        item.setText(_translate("DockWidget", "Hello", None))
        item = self.tableWidgetDis.item(1, 0)
        item.setText(_translate("DockWidget", "1,45", None))
        item = self.tableWidgetDis.item(1, 1)
        item.setText(_translate("DockWidget", "Olá", None))
        item = self.tableWidgetDis.item(2, 0)
        item.setText(_translate("DockWidget", "12/12/2012", None))
        item = self.tableWidgetDis.item(2, 1)
        item.setText(_translate("DockWidget", "Oui", None))
        self.tableWidgetDis.setSortingEnabled(__sortingEnabled)

