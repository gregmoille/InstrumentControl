# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UITranmission.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1073, 1031)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QToolTip {\n"
"    border: 1px solid #76797C;\n"
"    background-color: #5A7566;\n"
"    color: white;\n"
"    padding: 0px;                /*remove padding, for fix combobox tooltip.*/\n"
"    opacity: 200;\n"
"}\n"
"\n"
"QWidget {\n"
"    color: #eff0f1;\n"
"    background-color: #31363b;\n"
"    selection-background-color: #3daee9;\n"
"    selection-color: #eff0f1;\n"
"    background-clip: border;\n"
"    border-image: none;\n"
"    border: 0px transparent black;\n"
"    outline: 0;\n"
"}\n"
"\n"
"QWidget:item:hover {\n"
"    background-color: #18465d;\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QWidget:item:selected {\n"
"    background-color: #18465d;\n"
"}\n"
"\n"
"QCheckBox {\n"
"    spacing: 5px;\n"
"    outline: none;\n"
"    color: #eff0f1;\n"
"    margin-bottom: 2px;\n"
"}\n"
"\n"
"QCheckBox:disabled {\n"
"    color: #76797C;\n"
"}\n"
"\n"
"QCheckBox::indicator,\n"
"QGroupBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"}\n"
"\n"
"QGroupBox::indicator {\n"
"    margin-left: 2px;\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    image: url(:/qss_icons/rc/checkbox_unchecked.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked:hover,\n"
"QCheckBox::indicator:unchecked:pressed,\n"
"QGroupBox::indicator:unchecked:hover,\n"
"QGroupBox::indicator:unchecked:pressed {\n"
"    border: none;\n"
"    image: url(:/qss_icons/rc/checkbox_unchecked_focus.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(:/qss_icons/rc/checkbox_checked_focus.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:hover,\n"
"QCheckBox::indicator:checked:pressed,\n"
"QGroupBox::indicator:checked:hover,\n"
"QGroupBox::indicator:checked:pressed {\n"
"    border: none;\n"
"    image: url(:/qss_icons/rc/checkbox_checked_focus.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:indeterminate {\n"
"    image: url(:/qss_icons/rc/checkbox_indeterminate.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:indeterminate:hover,\n"
"QCheckBox::indicator:indeterminate:pressed {\n"
"    image: url(:/qss_icons/rc/checkbox_indeterminate_focus.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:disabled,\n"
"QGroupBox::indicator:checked:disabled {\n"
"    image: url(:/qss_icons/rc/checkbox_checked_disabled.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked:disabled,\n"
"QGroupBox::indicator:unchecked:disabled {\n"
"    image: url(:/qss_icons/rc/checkbox_unchecked_disabled.png);\n"
"}\n"
"\n"
"QRadioButton {\n"
"    spacing: 5px;\n"
"    outline: none;\n"
"    color: #eff0f1;\n"
"    margin-bottom: 2px;\n"
"}\n"
"\n"
"QRadioButton:disabled {\n"
"    color: #76797C;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 21px;\n"
"    height: 21px;\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"    image: url(:/qss_icons/rc/radio_unchecked.png);\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked:hover,\n"
"QRadioButton::indicator:unchecked:pressed {\n"
"    border: none;\n"
"    outline: none;\n"
"    image: url(:/qss_icons/rc/radio_unchecked_focus.png);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    border: none;\n"
"    outline: none;\n"
"    image: url(:/qss_icons/rc/radio_checked.png);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:hover,\n"
"QRadioButton::indicator:checked:pressed {\n"
"    border: none;\n"
"    outline: none;\n"
"    image: url(:/qss_icons/rc/radio_checked_focus.png);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:disabled {\n"
"    outline: none;\n"
"    image: url(:/qss_icons/rc/radio_checked_disabled.png);\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked:disabled {\n"
"    image: url(:/qss_icons/rc/radio_unchecked_disabled.png);\n"
"}\n"
"\n"
"QMenuBar {\n"
"    background-color: #31363b;\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background: transparent;\n"
"    border: 1px solid #76797C;\n"
"}\n"
"\n"
"QMenuBar::item:pressed {\n"
"    border: 1px solid #76797C;\n"
"    background-color: #3daee9;\n"
"    color: #eff0f1;\n"
"    margin-bottom: -1px;\n"
"    padding-bottom: 1px;\n"
"}\n"
"\n"
"QMenu {\n"
"    border: 1px solid #76797C;\n"
"    color: #eff0f1;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QMenu::icon {\n"
"    margin: 5px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    padding: 5px 30px 5px 30px;\n"
"    border: 1px solid transparent;\n"
"    /* reserve space for selection border */\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QMenu::separator {\n"
"    height: 2px;\n"
"    background: lightblue;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QMenu::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"}\n"
"\n"
"\n"
"/* non-exclusive indicator = check box style indicator\n"
"   (see QActionGroup::setExclusive) */\n"
"\n"
"QMenu::indicator:non-exclusive:unchecked {\n"
"    image: url(:/qss_icons/rc/checkbox_unchecked.png);\n"
"}\n"
"\n"
"QMenu::indicator:non-exclusive:unchecked:selected {\n"
"    image: url(:/qss_icons/rc/checkbox_unchecked_disabled.png);\n"
"}\n"
"\n"
"QMenu::indicator:non-exclusive:checked {\n"
"    image: url(:/qss_icons/rc/checkbox_checked_focus.png);\n"
"}\n"
"\n"
"QMenu::indicator:non-exclusive:checked:selected {\n"
"    image: url(:/qss_icons/rc/checkbox_checked_disabled.png);\n"
"}\n"
"\n"
"\n"
"/* exclusive indicator = radio button style indicator (see QActionGroup::setExclusive) */\n"
"\n"
"QMenu::indicator:exclusive:unchecked {\n"
"    image: url(:/qss_icons/rc/radio_unchecked.png);\n"
"}\n"
"\n"
"QMenu::indicator:exclusive:unchecked:selected {\n"
"    image: url(:/qss_icons/rc/radio_unchecked_disabled.png);\n"
"}\n"
"\n"
"QMenu::indicator:exclusive:checked {\n"
"    image: url(:/qss_icons/rc/radio_checked.png);\n"
"}\n"
"\n"
"QMenu::indicator:exclusive:checked:selected {\n"
"    image: url(:/qss_icons/rc/radio_checked_disabled.png);\n"
"}\n"
"\n"
"QMenu::right-arrow {\n"
"    margin: 5px;\n"
"    image: url(:/qss_icons/rc/right_arrow.png)\n"
"}\n"
"\n"
"QWidget:disabled {\n"
"    color: #454545;\n"
"    background-color: #31363b;\n"
"}\n"
"\n"
"QAbstractItemView {\n"
"    alternate-background-color: #31363b;\n"
"    color: #eff0f1;\n"
"    border: 1px solid #3A3939;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QWidget:focus,\n"
"QMenuBar:focus {\n"
"    border: 1px solid #3daee9;\n"
"}\n"
"\n"
"QTabWidget:focus,\n"
"QCheckBox:focus,\n"
"QRadioButton:focus,\n"
"QSlider:focus {\n"
"    border: none;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: #232629;\n"
"    padding: 5px;\n"
"    border-style: solid;\n"
"    border: 1px solid #76797C;\n"
"    border-radius: 2px;\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QAbstractItemView QLineEdit {\n"
"    padding: 0;\n"
"}\n"
"\n"
"QGroupBox {\n"
"    border: 1px solid #76797C;\n"
"    border-radius: 2px;\n"
"    margin-top: 20px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 10px;\n"
"}\n"
"\n"
"QAbstractScrollArea {\n"
"    border-radius: 2px;\n"
"    border: 1px solid #76797C;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    height: 15px;\n"
"    margin: 3px 15px 3px 15px;\n"
"    border: 1px transparent #2A2929;\n"
"    border-radius: 4px;\n"
"    background-color: #2A2929;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background-color: #605F5F;\n"
"    min-width: 5px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"    margin: 0px 3px 0px 3px;\n"
"    border-image: url(:/qss_icons/rc/right_arrow_disabled.png);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    margin: 0px 3px 0px 3px;\n"
"    border-image: url(:/qss_icons/rc/left_arrow_disabled.png);\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal:hover,\n"
"QScrollBar::add-line:horizontal:on {\n"
"    border-image: url(:/qss_icons/rc/right_arrow.png);\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal:hover,\n"
"QScrollBar::sub-line:horizontal:on {\n"
"    border-image: url(:/qss_icons/rc/left_arrow.png);\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:horizontal,\n"
"QScrollBar::down-arrow:horizontal {\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal,\n"
"QScrollBar::sub-page:horizontal {\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background-color: #2A2929;\n"
"    width: 15px;\n"
"    margin: 15px 3px 15px 3px;\n"
"    border: 1px transparent #2A2929;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background-color: #605F5F;\n"
"    min-height: 5px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"    margin: 3px 0px 3px 0px;\n"
"    border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"    margin: 3px 0px 3px 0px;\n"
"    border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical:hover,\n"
"QScrollBar::sub-line:vertical:on {\n"
"    border-image: url(:/qss_icons/rc/up_arrow.png);\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical:hover,\n"
"QScrollBar::add-line:vertical:on {\n"
"    border-image: url(:/qss_icons/rc/down_arrow.png);\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical,\n"
"QScrollBar::down-arrow:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"QTextEdit {\n"
"    background-color: #232629;\n"
"    color: #eff0f1;\n"
"    border: 1px solid #76797C;\n"
"}\n"
"\n"
"QPlainTextEdit {\n"
"    background-color: #232629;\n"
"    ;\n"
"    color: #eff0f1;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #76797C;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #76797C;\n"
"    color: #eff0f1;\n"
"    padding: 5px;\n"
"    border: 1px solid #76797C;\n"
"}\n"
"\n"
"QSizeGrip {\n"
"    image: url(:/qss_icons/rc/sizegrip.png);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QMainWindow::separator {\n"
"    background-color: #31363b;\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    spacing: 2px;\n"
"    border: 1px dashed #76797C;\n"
"}\n"
"\n"
"QMainWindow::separator:hover {\n"
"    background-color: #787876;\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #76797C;\n"
"    spacing: 2px;\n"
"}\n"
"\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background-color: #76797C;\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QFrame {\n"
"    border-radius: 2px;\n"
"    border: 1px solid #76797C;\n"
"}\n"
"\n"
"QFrame[frameShape=\"0\"] {\n"
"    border-radius: 2px;\n"
"    border: 1px transparent #76797C;\n"
"}\n"
"\n"
"QStackedWidget {\n"
"    border: 1px transparent black;\n"
"}\n"
"\n"
"QToolBar {\n"
"    border: 1px transparent #393838;\n"
"    background: 1px solid #31363b;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QToolBar::handle:horizontal {\n"
"    image: url(:/qss_icons/rc/Hmovetoolbar.png);\n"
"}\n"
"\n"
"QToolBar::handle:vertical {\n"
"    image: url(:/qss_icons/rc/Vmovetoolbar.png);\n"
"}\n"
"\n"
"QToolBar::separator:horizontal {\n"
"    image: url(:/qss_icons/rc/Hsepartoolbar.png);\n"
"}\n"
"\n"
"QToolBar::separator:vertical {\n"
"    image: url(:/qss_icons/rc/Vsepartoolbar.png);\n"
"}\n"
"\n"
"QToolButton#qt_toolbar_ext_button {\n"
"    background: #58595a\n"
"}\n"
"\n"
"QPushButton {\n"
"    color: #eff0f1;\n"
"    background-color: #31363b;\n"
"    border-width: 1px;\n"
"    border-color: #76797C;\n"
"    border-style: solid;\n"
"    padding: 5px;\n"
"    border-radius: 2px;\n"
"    outline: none;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #31363b;\n"
"    border-width: 1px;\n"
"    border-color: #454545;\n"
"    border-style: solid;\n"
"    padding-top: 5px;\n"
"    padding-bottom: 5px;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    border-radius: 2px;\n"
"    color: #454545;\n"
"}\n"
"\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3daee9;\n"
"    padding-top: -15px;\n"
"    padding-bottom: -17px;\n"
"}\n"
"\n"
"QComboBox {\n"
"    selection-background-color: #3daee9;\n"
"    border-style: solid;\n"
"    border: 1px solid #76797C;\n"
"    border-radius: 2px;\n"
"    padding: 5px;\n"
"    min-width: 75px;\n"
"}\n"
"\n"
"QComboBox:hover,\n"
"QPushButton:hover,\n"
"QAbstractSpinBox:hover,\n"
"QLineEdit:hover,\n"
"QTextEdit:hover,\n"
"QPlainTextEdit:hover,\n"
"QAbstractView:hover,\n"
"QTreeView:hover {\n"
"    border: 1px solid #3daee9;\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    selection-background-color: #4a4a4a;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #232629;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #76797C;\n"
"    selection-background-color: #18465d;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left-width: 0px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on,\n"
"QComboBox::down-arrow:hover,\n"
"QComboBox::down-arrow:focus {\n"
"    image: url(:/qss_icons/rc/down_arrow.png);\n"
"}\n"
"\n"
"QAbstractSpinBox {\n"
"    padding: 5px;\n"
"    border: 1px solid #76797C;\n"
"    background-color: #232629;\n"
"    color: #eff0f1;\n"
"    border-radius: 2px;\n"
"    min-width: 75px;\n"
"}\n"
"\n"
"QAbstractSpinBox:up-button {\n"
"    background-color: transparent;\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: center right;\n"
"}\n"
"\n"
"QAbstractSpinBox:down-button {\n"
"    background-color: transparent;\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: center left;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-arrow,\n"
"QAbstractSpinBox::up-arrow:disabled,\n"
"QAbstractSpinBox::up-arrow:off {\n"
"    image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-arrow:hover {\n"
"    image: url(:/qss_icons/rc/up_arrow.png);\n"
"}\n"
"\n"
"QAbstractSpinBox::down-arrow,\n"
"QAbstractSpinBox::down-arrow:disabled,\n"
"QAbstractSpinBox::down-arrow:off {\n"
"    image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"\n"
"QAbstractSpinBox::down-arrow:hover {\n"
"    image: url(:/qss_icons/rc/down_arrow.png);\n"
"}\n"
"\n"
"QLabel {\n"
"    border: 0px solid black;\n"
"}\n"
"\n"
"QTabWidget {\n"
"    border: 0px transparent black;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #76797C;\n"
"    padding: 5px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    /* left: 5px; move to the right by 5px */\n"
"}\n"
"\n"
"QTabBar {\n"
"    qproperty-drawBase: 0;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QTabBar:focus {\n"
"    border: 0px transparent black;\n"
"}\n"
"\n"
"QTabBar::close-button {\n"
"    image: url(:/qss_icons/rc/close.png);\n"
"    background: transparent;\n"
"}\n"
"\n"
"QTabBar::close-button:hover {\n"
"    image: url(:/qss_icons/rc/close-hover.png);\n"
"    background: transparent;\n"
"}\n"
"\n"
"QTabBar::close-button:pressed {\n"
"    image: url(:/qss_icons/rc/close-pressed.png);\n"
"    background: transparent;\n"
"}\n"
"\n"
"\n"
"/* TOP TABS */\n"
"\n"
"QTabBar::tab:top {\n"
"    color: #eff0f1;\n"
"    border: 1px solid #76797C;\n"
"    border-bottom: 1px transparent black;\n"
"    background-color: #31363b;\n"
"    padding: 5px;\n"
"    min-width: 50px;\n"
"    border-top-left-radius: 2px;\n"
"    border-top-right-radius: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:top:selected {\n"
"    color: #eff0f1;\n"
"    background-color: #54575B;\n"
"    border: 1px solid #76797C;\n"
"    border-bottom: 2px solid #3daee9;\n"
"    border-top-left-radius: 2px;\n"
"    border-top-right-radius: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:top:!selected:hover {\n"
"    background-color: #3daee9;\n"
"}\n"
"\n"
"\n"
"/* BOTTOM TABS */\n"
"\n"
"QTabBar::tab:bottom {\n"
"    color: #eff0f1;\n"
"    border: 1px solid #76797C;\n"
"    border-top: 1px transparent black;\n"
"    background-color: #31363b;\n"
"    padding: 5px;\n"
"    border-bottom-left-radius: 2px;\n"
"    border-bottom-right-radius: 2px;\n"
"    min-width: 50px;\n"
"}\n"
"\n"
"QTabBar::tab:bottom:selected {\n"
"    color: #eff0f1;\n"
"    background-color: #54575B;\n"
"    border: 1px solid #76797C;\n"
"    border-top: 2px solid #3daee9;\n"
"    border-bottom-left-radius: 2px;\n"
"    border-bottom-right-radius: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:bottom:!selected:hover {\n"
"    background-color: #3daee9;\n"
"}\n"
"\n"
"\n"
"/* LEFT TABS */\n"
"\n"
"QTabBar::tab:left {\n"
"    color: #eff0f1;\n"
"    border: 1px solid #76797C;\n"
"    border-left: 1px transparent black;\n"
"    background-color: #31363b;\n"
"    padding: 5px;\n"
"    border-top-right-radius: 2px;\n"
"    border-bottom-right-radius: 2px;\n"
"    min-height: 50px;\n"
"}\n"
"\n"
"QTabBar::tab:left:selected {\n"
"    color: #eff0f1;\n"
"    background-color: #54575B;\n"
"    border: 1px solid #76797C;\n"
"    border-left: 2px solid #3daee9;\n"
"    border-top-right-radius: 2px;\n"
"    border-bottom-right-radius: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:left:!selected:hover {\n"
"    background-color: #3daee9;\n"
"}\n"
"\n"
"\n"
"/* RIGHT TABS */\n"
"\n"
"QTabBar::tab:right {\n"
"    color: #eff0f1;\n"
"    border: 1px solid #76797C;\n"
"    border-right: 1px transparent black;\n"
"    background-color: #31363b;\n"
"    padding: 5px;\n"
"    border-top-left-radius: 2px;\n"
"    border-bottom-left-radius: 2px;\n"
"    min-height: 50px;\n"
"}\n"
"\n"
"QTabBar::tab:right:selected {\n"
"    color: #eff0f1;\n"
"    background-color: #54575B;\n"
"    border: 1px solid #76797C;\n"
"    border-right: 2px solid #3daee9;\n"
"    border-top-left-radius: 2px;\n"
"    border-bottom-left-radius: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:right:!selected:hover {\n"
"    background-color: #3daee9;\n"
"}\n"
"\n"
"QTabBar QToolButton::right-arrow:enabled {\n"
"    image: url(:/qss_icons/rc/right_arrow.png);\n"
"}\n"
"\n"
"QTabBar QToolButton::left-arrow:enabled {\n"
"    image: url(:/qss_icons/rc/left_arrow.png);\n"
"}\n"
"\n"
"QTabBar QToolButton::right-arrow:disabled {\n"
"    image: url(:/qss_icons/rc/right_arrow_disabled.png);\n"
"}\n"
"\n"
"QTabBar QToolButton::left-arrow:disabled {\n"
"    image: url(:/qss_icons/rc/left_arrow_disabled.png);\n"
"}\n"
"\n"
"QDockWidget {\n"
"    background: #31363b;\n"
"    border: 1px solid #403F3F;\n"
"    titlebar-close-icon: url(:/qss_icons/rc/close.png);\n"
"    titlebar-normal-icon: url(:/qss_icons/rc/undock.png);\n"
"}\n"
"\n"
"QDockWidget::close-button,\n"
"QDockWidget::float-button {\n"
"    border: 1px solid transparent;\n"
"    border-radius: 2px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QDockWidget::close-button:hover,\n"
"QDockWidget::float-button:hover {\n"
"    background: rgba(255, 255, 255, 10);\n"
"}\n"
"\n"
"QDockWidget::close-button:pressed,\n"
"QDockWidget::float-button:pressed {\n"
"    padding: 1px -1px -1px 1px;\n"
"    background: rgba(255, 255, 255, 10);\n"
"}\n"
"\n"
"QTreeView,\n"
"QListView {\n"
"    border: 1px solid #76797C;\n"
"    background-color: #232629;\n"
"}\n"
"\n"
"QTreeView:branch:selected,\n"
"QTreeView:branch:hover {\n"
"    background: url(:/qss_icons/rc/transparent.png);\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:!adjoins-item {\n"
"    border-image: url(:/qss_icons/rc/transparent.png);\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:adjoins-item {\n"
"    border-image: url(:/qss_icons/rc/transparent.png);\n"
"}\n"
"\n"
"QTreeView::branch:!has-children:!has-siblings:adjoins-item {\n"
"    border-image: url(:/qss_icons/rc/transparent.png);\n"
"}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings {\n"
"    image: url(:/qss_icons/rc/branch_closed.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings {\n"
"    image: url(:/qss_icons/rc/branch_open.png);\n"
"}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed:hover,\n"
"QTreeView::branch:closed:has-children:has-siblings:hover {\n"
"    image: url(:/qss_icons/rc/branch_closed-on.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings:hover,\n"
"QTreeView::branch:open:has-children:has-siblings:hover {\n"
"    image: url(:/qss_icons/rc/branch_open-on.png);\n"
"}\n"
"\n"
"QListView::item:!selected:hover,\n"
"QTreeView::item:!selected:hover {\n"
"    background: #18465d;\n"
"    outline: 0;\n"
"    color: #eff0f1\n"
"}\n"
"\n"
"QListView::item:selected:hover,\n"
"QTreeView::item:selected:hover {\n"
"    background: #287399;\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QTreeView::indicator:checked,\n"
"QListView::indicator:checked {\n"
"    image: url(:/qss_icons/rc/checkbox_checked.png);\n"
"}\n"
"\n"
"QTreeView::indicator:unchecked,\n"
"QListView::indicator:unchecked {\n"
"    image: url(:/qss_icons/rc/checkbox_unchecked.png);\n"
"}\n"
"\n"
"QTreeView::indicator:checked:hover,\n"
"QTreeView::indicator:checked:focus,\n"
"QTreeView::indicator:checked:pressed,\n"
"QListView::indicator:checked:hover,\n"
"QListView::indicator:checked:focus,\n"
"QListView::indicator:checked:pressed {\n"
"    image: url(:/qss_icons/rc/checkbox_checked_focus.png);\n"
"}\n"
"\n"
"QTreeView::indicator:unchecked:hover,\n"
"QTreeView::indicator:unchecked:focus,\n"
"QTreeView::indicator:unchecked:pressed,\n"
"QListView::indicator:unchecked:hover,\n"
"QListView::indicator:unchecked:focus,\n"
"QListView::indicator:unchecked:pressed {\n"
"    image: url(:/qss_icons/rc/checkbox_unchecked_focus.png);\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #565a5e;\n"
"    height: 4px;\n"
"    background: #565a5e;\n"
"    margin: 0px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #232629;\n"
"    border: 1px solid #565a5e;\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    margin: -8px 0;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border: 1px solid #565a5e;\n"
"    width: 4px;\n"
"    background: #565a5e;\n"
"    margin: 0px;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    background: #232629;\n"
"    border: 1px solid #565a5e;\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    margin: 0 -8px;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"QToolButton {\n"
"    background-color: transparent;\n"
"    border: 1px transparent #76797C;\n"
"    border-radius: 2px;\n"
"    margin: 3px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QToolButton[popupMode=\"1\"] {\n"
"    /* only for MenuButtonPopup */\n"
"    padding-right: 20px;\n"
"    /* make way for the popup button */\n"
"    border: 1px #76797C;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QToolButton[popupMode=\"2\"] {\n"
"    /* only for InstantPopup */\n"
"    padding-right: 10px;\n"
"    /* make way for the popup button */\n"
"    border: 1px #76797C;\n"
"}\n"
"\n"
"QToolButton:hover,\n"
"QToolButton::menu-button:hover {\n"
"    background-color: transparent;\n"
"    border: 1px solid #3daee9;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QToolButton:checked,\n"
"QToolButton:pressed,\n"
"QToolButton::menu-button:pressed {\n"
"    background-color: #3daee9;\n"
"    border: 1px solid #3daee9;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"\n"
"/* the subcontrol below is used only in the InstantPopup or DelayedPopup mode */\n"
"\n"
"QToolButton::menu-indicator {\n"
"    image: url(:/qss_icons/rc/down_arrow.png);\n"
"    top: -7px;\n"
"    left: -2px;\n"
"    /* shift it a bit */\n"
"}\n"
"\n"
"\n"
"/* the subcontrols below are used only in the MenuButtonPopup mode */\n"
"\n"
"QToolButton::menu-button {\n"
"    border: 1px transparent #76797C;\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"    /* 16px width + 4px for border = 20px allocated above */\n"
"    width: 16px;\n"
"    outline: none;\n"
"}\n"
"\n"
"QToolButton::menu-arrow {\n"
"    image: url(:/qss_icons/rc/down_arrow.png);\n"
"}\n"
"\n"
"QToolButton::menu-arrow:open {\n"
"    border: 1px solid #76797C;\n"
"}\n"
"\n"
"QPushButton::menu-indicator {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: bottom right;\n"
"    left: 8px;\n"
"}\n"
"\n"
"QTableView {\n"
"    border: 1px solid #76797C;\n"
"    gridline-color: #31363b;\n"
"    background-color: #232629;\n"
"}\n"
"\n"
"QTableView,\n"
"QHeaderView {\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"QTableView::item:pressed,\n"
"QListView::item:pressed,\n"
"QTreeView::item:pressed {\n"
"    background: #18465d;\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QTableView::item:selected:active,\n"
"QTreeView::item:selected:active,\n"
"QListView::item:selected:active {\n"
"    background: #287399;\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QHeaderView {\n"
"    background-color: #31363b;\n"
"    border: 1px transparent;\n"
"    border-radius: 0px;\n"
"    margin: 0px;\n"
"    padding: 0px;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #31363b;\n"
"    color: #eff0f1;\n"
"    padding: 5px;\n"
"    border: 1px solid #76797C;\n"
"    border-radius: 0px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QHeaderView::section::vertical::first,\n"
"QHeaderView::section::vertical::only-one {\n"
"    border-top: 1px solid #76797C;\n"
"}\n"
"\n"
"QHeaderView::section::vertical {\n"
"    border-top: transparent;\n"
"}\n"
"\n"
"QHeaderView::section::horizontal::first,\n"
"QHeaderView::section::horizontal::only-one {\n"
"    border-left: 1px solid #76797C;\n"
"}\n"
"\n"
"QHeaderView::section::horizontal {\n"
"    border-left: transparent;\n"
"}\n"
"\n"
"QHeaderView::section:checked {\n"
"    color: white;\n"
"    background-color: #334e5e;\n"
"}\n"
"\n"
"\n"
"/* style the sort indicator */\n"
"\n"
"QHeaderView::down-arrow {\n"
"    image: url(:/qss_icons/rc/down_arrow.png);\n"
"}\n"
"\n"
"QHeaderView::up-arrow {\n"
"    image: url(:/qss_icons/rc/up_arrow.png);\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #31363b;\n"
"    border: 1px transparent #76797C;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"QToolBox {\n"
"    padding: 5px;\n"
"    border: 1px transparent black;\n"
"}\n"
"\n"
"QToolBox::tab {\n"
"    color: #eff0f1;\n"
"    background-color: #31363b;\n"
"    border: 1px solid #76797C;\n"
"    border-bottom: 1px transparent #31363b;\n"
"    border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"}\n"
"\n"
"QToolBox::tab:selected {\n"
"    /* italicize selected tabs */\n"
"    font: italic;\n"
"    background-color: #31363b;\n"
"    border-color: #3daee9;\n"
"}\n"
"\n"
"QStatusBar::item {\n"
"    border: 0px transparent dark;\n"
"}\n"
"\n"
"QFrame[height=\"3\"],\n"
"QFrame[width=\"3\"] {\n"
"    background-color: #76797C;\n"
"}\n"
"\n"
"QSplitter::handle {\n"
"    border: 1px dashed #76797C;\n"
"}\n"
"\n"
"QSplitter::handle:hover {\n"
"    background-color: #787876;\n"
"    border: 1px solid #76797C;\n"
"}\n"
"\n"
"QSplitter::handle:horizontal {\n"
"    width: 1px;\n"
"}\n"
"\n"
"QSplitter::handle:vertical {\n"
"    height: 1px;\n"
"}\n"
"\n"
"QProgressBar {\n"
"    border: 1px solid #76797C;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #05B8CC;\n"
"}\n"
"\n"
"QDateEdit {\n"
"    selection-background-color: #3daee9;\n"
"    border-style: solid;\n"
"    border: 1px solid #3375A3;\n"
"    border-radius: 2px;\n"
"    padding: 1px;\n"
"    min-width: 75px;\n"
"}\n"
"\n"
"QDateEdit:on {\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    selection-background-color: #4a4a4a;\n"
"}\n"
"\n"
"QDateEdit QAbstractItemView {\n"
"    background-color: #232629;\n"
"    border-radius: 2px;\n"
"    border: 1px solid #3375A3;\n"
"    selection-background-color: #3daee9;\n"
"}\n"
"\n"
"QDateEdit::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left-width: 0px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QDateEdit::down-arrow {\n"
"    image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
"}\n"
"\n"
"QDateEdit::down-arrow:on,\n"
"QDateEdit::down-arrow:hover,\n"
"QDateEdit::down-arrow:focus {\n"
"    image: url(:/qss_icons/rc/down_arrow.png);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_13 = QtWidgets.QWidget(self.centralwidget)
        self.widget_13.setObjectName("widget_13")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.widget_13)
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_13)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_13.addWidget(self.pushButton_2, 0, 5, 1, 1)
        self.led_SetWavelength_2 = QtWidgets.QLabel(self.widget_13)
        self.led_SetWavelength_2.setMinimumSize(QtCore.QSize(20, 20))
        self.led_SetWavelength_2.setMaximumSize(QtCore.QSize(20, 20))
        self.led_SetWavelength_2.setText("")
        self.led_SetWavelength_2.setPixmap(QtGui.QPixmap(":/qss_icons/rc/radio_checked.png"))
        self.led_SetWavelength_2.setScaledContents(True)
        self.led_SetWavelength_2.setObjectName("led_SetWavelength_2")
        self.gridLayout_13.addWidget(self.led_SetWavelength_2, 0, 6, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem, 0, 0, 1, 1)
        self.but_connect = QtWidgets.QPushButton(self.widget_13)
        self.but_connect.setCheckable(True)
        self.but_connect.setChecked(True)
        self.but_connect.setObjectName("but_connect")
        self.gridLayout_13.addWidget(self.but_connect, 0, 2, 1, 1)
        self.led_SetWavelength_3 = QtWidgets.QLabel(self.widget_13)
        self.led_SetWavelength_3.setEnabled(True)
        self.led_SetWavelength_3.setMinimumSize(QtCore.QSize(20, 20))
        self.led_SetWavelength_3.setMaximumSize(QtCore.QSize(20, 20))
        self.led_SetWavelength_3.setText("")
        self.led_SetWavelength_3.setPixmap(QtGui.QPixmap(":/qss_icons/rc/radio_checked.png"))
        self.led_SetWavelength_3.setScaledContents(True)
        self.led_SetWavelength_3.setObjectName("led_SetWavelength_3")
        self.gridLayout_13.addWidget(self.led_SetWavelength_3, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem1, 0, 7, 1, 1)
        self.comboBox_6 = QtWidgets.QComboBox(self.widget_13)
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItem("")
        self.gridLayout_13.addWidget(self.comboBox_6, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem2, 0, 4, 1, 1)
        self.verticalLayout.addWidget(self.widget_13)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(9)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_5 = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setContentsMargins(-1, 9, -1, 9)
        self.verticalLayout_6.setSpacing(9)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_11 = QtWidgets.QWidget(self.groupBox_5)
        self.widget_11.setObjectName("widget_11")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.widget_11)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setHorizontalSpacing(9)
        self.gridLayout_9.setVerticalSpacing(0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_18 = QtWidgets.QLabel(self.widget_11)
        self.label_18.setMinimumSize(QtCore.QSize(0, 15))
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_18.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.gridLayout_9.addWidget(self.label_18, 0, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.widget_11)
        self.label_19.setMinimumSize(QtCore.QSize(0, 15))
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_19.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.gridLayout_9.addWidget(self.label_19, 0, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.widget_11)
        self.label_20.setMinimumSize(QtCore.QSize(0, 15))
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_20.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.gridLayout_9.addWidget(self.label_20, 0, 2, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.widget_11)
        self.comboBox_2.setMinimumSize(QtCore.QSize(87, 0))
        self.comboBox_2.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_9.addWidget(self.comboBox_2, 1, 0, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.widget_11)
        self.comboBox_3.setMinimumSize(QtCore.QSize(87, 0))
        self.comboBox_3.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout_9.addWidget(self.comboBox_3, 1, 1, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(self.widget_11)
        self.comboBox_4.setMinimumSize(QtCore.QSize(87, 0))
        self.comboBox_4.setMaximumSize(QtCore.QSize(120, 16777215))
        self.comboBox_4.setSizeIncrement(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_4.setFont(font)
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout_9.addWidget(self.comboBox_4, 1, 2, 1, 1)
        self.verticalLayout_6.addWidget(self.widget_11)
        self.widget_12 = QtWidgets.QWidget(self.groupBox_5)
        self.widget_12.setObjectName("widget_12")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.widget_12)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setHorizontalSpacing(9)
        self.gridLayout_10.setVerticalSpacing(0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.spnbx_daq_Vmin = QtWidgets.QDoubleSpinBox(self.widget_12)
        self.spnbx_daq_Vmin.setMinimumSize(QtCore.QSize(87, 0))
        self.spnbx_daq_Vmin.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_daq_Vmin.setFont(font)
        self.spnbx_daq_Vmin.setObjectName("spnbx_daq_Vmin")
        self.gridLayout_10.addWidget(self.spnbx_daq_Vmin, 1, 0, 1, 1)
        self.spnbx_daq_Vmax = QtWidgets.QDoubleSpinBox(self.widget_12)
        self.spnbx_daq_Vmax.setMinimumSize(QtCore.QSize(87, 0))
        self.spnbx_daq_Vmax.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_daq_Vmax.setFont(font)
        self.spnbx_daq_Vmax.setObjectName("spnbx_daq_Vmax")
        self.gridLayout_10.addWidget(self.spnbx_daq_Vmax, 1, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.widget_12)
        self.label_21.setMinimumSize(QtCore.QSize(0, 15))
        self.label_21.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.gridLayout_10.addWidget(self.label_21, 0, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.widget_12)
        self.label_22.setMinimumSize(QtCore.QSize(0, 15))
        self.label_22.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.gridLayout_10.addWidget(self.label_22, 0, 1, 1, 1)
        self.comboBox_8 = QtWidgets.QComboBox(self.widget_12)
        self.comboBox_8.setMinimumSize(QtCore.QSize(87, 0))
        self.comboBox_8.setMaximumSize(QtCore.QSize(120, 16777215))
        self.comboBox_8.setObjectName("comboBox_8")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.gridLayout_10.addWidget(self.comboBox_8, 1, 2, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.widget_12)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.gridLayout_10.addWidget(self.label_28, 0, 2, 1, 1)
        self.verticalLayout_6.addWidget(self.widget_12)
        self.gridLayout.addWidget(self.groupBox_5, 2, 3, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setContentsMargins(-1, 9, -1, 9)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_4 = QtWidgets.QWidget(self.groupBox)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 15))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 15))
        self.label.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.led_SetWavelength = QtWidgets.QLabel(self.widget_4)
        self.led_SetWavelength.setMinimumSize(QtCore.QSize(20, 20))
        self.led_SetWavelength.setMaximumSize(QtCore.QSize(20, 20))
        self.led_SetWavelength.setText("")
        self.led_SetWavelength.setPixmap(QtGui.QPixmap(":/qss_icons/rc/radio_checked.png"))
        self.led_SetWavelength.setScaledContents(True)
        self.led_SetWavelength.setObjectName("led_SetWavelength")
        self.gridLayout_2.addWidget(self.led_SetWavelength, 1, 1, 1, 1)
        self.spnbx_I = QtWidgets.QDoubleSpinBox(self.widget_4)
        self.spnbx_I.setMinimumSize(QtCore.QSize(87, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_I.setFont(font)
        self.spnbx_I.setAlignment(QtCore.Qt.AlignCenter)
        self.spnbx_I.setKeyboardTracking(False)
        self.spnbx_I.setMaximum(200.0)
        self.spnbx_I.setProperty("value", 140.0)
        self.spnbx_I.setObjectName("spnbx_I")
        self.gridLayout_2.addWidget(self.spnbx_I, 1, 2, 1, 1)
        self.spnbx_lbd = QtWidgets.QDoubleSpinBox(self.widget_4)
        self.spnbx_lbd.setMinimumSize(QtCore.QSize(87, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_lbd.setFont(font)
        self.spnbx_lbd.setAlignment(QtCore.Qt.AlignCenter)
        self.spnbx_lbd.setKeyboardTracking(False)
        self.spnbx_lbd.setDecimals(3)
        self.spnbx_lbd.setMaximum(20000.0)
        self.spnbx_lbd.setProperty("value", 1550.0)
        self.spnbx_lbd.setObjectName("spnbx_lbd")
        self.gridLayout_2.addWidget(self.spnbx_lbd, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setMinimumSize(QtCore.QSize(0, 15))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.widget_9 = QtWidgets.QWidget(self.groupBox)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_9)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.spnbx_pzt = QtWidgets.QDoubleSpinBox(self.widget_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_pzt.setFont(font)
        self.spnbx_pzt.setMouseTracking(True)
        self.spnbx_pzt.setAlignment(QtCore.Qt.AlignCenter)
        self.spnbx_pzt.setKeyboardTracking(False)
        self.spnbx_pzt.setDecimals(2)
        self.spnbx_pzt.setMaximum(100.0)
        self.spnbx_pzt.setObjectName("spnbx_pzt")
        self.verticalLayout_5.addWidget(self.spnbx_pzt)
        self.slide_pzt = QtWidgets.QSlider(self.widget_9)
        self.slide_pzt.setMaximum(10000)
        self.slide_pzt.setOrientation(QtCore.Qt.Horizontal)
        self.slide_pzt.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slide_pzt.setObjectName("slide_pzt")
        self.verticalLayout_5.addWidget(self.slide_pzt)
        self.verticalLayout_2.addWidget(self.widget_9)
        self.gridLayout.addWidget(self.groupBox, 1, 2, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setContentsMargins(0, 9, 0, 9)
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget1 = QtWidgets.QWidget(self.groupBox_4)
        self.widget1.setMinimumSize(QtCore.QSize(100, 0))
        self.widget1.setMaximumSize(QtCore.QSize(100, 16777215))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_8.addWidget(self.pushButton_4)
        self.checkBox_2 = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_2.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_8.addWidget(self.checkBox_2)
        self.horizontalLayout.addWidget(self.widget1)
        self.widget_3 = QtWidgets.QWidget(self.groupBox_4)
        self.widget_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setHorizontalSpacing(9)
        self.gridLayout_6.setVerticalSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_6.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_6.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.widget_3)
        self.label_15.setEnabled(False)
        self.label_15.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout_6.addWidget(self.label_15, 1, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget_3)
        self.label_8.setEnabled(False)
        self.label_8.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_6.addWidget(self.label_8, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget_3)
        self.gridLayout.addWidget(self.groupBox_4, 2, 2, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_11.setContentsMargins(-1, 9, -1, 9)
        self.gridLayout_11.setSpacing(9)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.lbl_wavemeterlbd = QtWidgets.QLabel(self.groupBox_6)
        self.lbl_wavemeterlbd.setEnabled(False)
        self.lbl_wavemeterlbd.setMinimumSize(QtCore.QSize(0, 15))
        self.lbl_wavemeterlbd.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_wavemeterlbd.setFont(font)
        self.lbl_wavemeterlbd.setObjectName("lbl_wavemeterlbd")
        self.gridLayout_11.addWidget(self.lbl_wavemeterlbd, 0, 3, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(87, 0))
        self.lineEdit_4.setMaximumSize(QtCore.QSize(87, 16777215))
        self.lineEdit_4.setSizeIncrement(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_11.addWidget(self.lineEdit_4, 1, 3, 1, 1)
        self.comboBox_5 = QtWidgets.QComboBox(self.groupBox_6)
        self.comboBox_5.setEnabled(False)
        self.comboBox_5.setMinimumSize(QtCore.QSize(87, 0))
        self.comboBox_5.setMaximumSize(QtCore.QSize(87, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_5.setFont(font)
        self.comboBox_5.setObjectName("comboBox_5")
        self.gridLayout_11.addWidget(self.comboBox_5, 1, 2, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.groupBox_6)
        self.label_25.setEnabled(False)
        self.label_25.setMinimumSize(QtCore.QSize(0, 15))
        self.label_25.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.gridLayout_11.addWidget(self.label_25, 0, 2, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.groupBox_6)
        self.label_26.setMinimumSize(QtCore.QSize(0, 15))
        self.label_26.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_26.setText("")
        self.label_26.setObjectName("label_26")
        self.gridLayout_11.addWidget(self.label_26, 2, 3, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_6)
        self.checkBox_4.setMinimumSize(QtCore.QSize(87, 0))
        self.checkBox_4.setMaximumSize(QtCore.QSize(87, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setCheckable(True)
        self.checkBox_4.setAutoRepeat(False)
        self.checkBox_4.setTristate(False)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_11.addWidget(self.checkBox_4, 2, 2, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_11.addWidget(self.pushButton_5, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_6, 2, 4, 1, 1)
        self.groupBox_DCscan = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_DCscan.sizePolicy().hasHeightForWidth())
        self.groupBox_DCscan.setSizePolicy(sizePolicy)
        self.groupBox_DCscan.setObjectName("groupBox_DCscan")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_DCscan)
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 9)
        self.verticalLayout_3.setSpacing(9)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_6 = QtWidgets.QWidget(self.groupBox_DCscan)
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_6)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 8)
        self.gridLayout_4.setSpacing(9)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.widget_6)
        self.label_4.setMinimumSize(QtCore.QSize(0, 15))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget_6)
        self.label_5.setMinimumSize(QtCore.QSize(0, 15))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget_6)
        self.label_6.setMinimumSize(QtCore.QSize(0, 15))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 2, 1, 1)
        self.spnbx_lbd_start = QtWidgets.QDoubleSpinBox(self.widget_6)
        self.spnbx_lbd_start.setMinimumSize(QtCore.QSize(87, 0))
        self.spnbx_lbd_start.setMaximumSize(QtCore.QSize(120, 87))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_lbd_start.setFont(font)
        self.spnbx_lbd_start.setAlignment(QtCore.Qt.AlignCenter)
        self.spnbx_lbd_start.setKeyboardTracking(True)
        self.spnbx_lbd_start.setMaximum(2000.0)
        self.spnbx_lbd_start.setProperty("value", 1530.0)
        self.spnbx_lbd_start.setObjectName("spnbx_lbd_start")
        self.gridLayout_4.addWidget(self.spnbx_lbd_start, 1, 0, 1, 1)
        self.spnbx_lbd_stop = QtWidgets.QDoubleSpinBox(self.widget_6)
        self.spnbx_lbd_stop.setMinimumSize(QtCore.QSize(87, 0))
        self.spnbx_lbd_stop.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_lbd_stop.setFont(font)
        self.spnbx_lbd_stop.setAlignment(QtCore.Qt.AlignCenter)
        self.spnbx_lbd_stop.setKeyboardTracking(True)
        self.spnbx_lbd_stop.setMaximum(1800.0)
        self.spnbx_lbd_stop.setProperty("value", 99.99)
        self.spnbx_lbd_stop.setObjectName("spnbx_lbd_stop")
        self.gridLayout_4.addWidget(self.spnbx_lbd_stop, 1, 1, 1, 1)
        self.spnbx_speed = QtWidgets.QDoubleSpinBox(self.widget_6)
        self.spnbx_speed.setMinimumSize(QtCore.QSize(87, 0))
        self.spnbx_speed.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_speed.setFont(font)
        self.spnbx_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.spnbx_speed.setKeyboardTracking(True)
        self.spnbx_speed.setDecimals(0)
        self.spnbx_speed.setProperty("value", 10.0)
        self.spnbx_speed.setObjectName("spnbx_speed")
        self.gridLayout_4.addWidget(self.spnbx_speed, 1, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.widget_6)
        self.label_7 = QtWidgets.QLabel(self.groupBox_DCscan)
        self.label_7.setMinimumSize(QtCore.QSize(0, 15))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.widget_7 = QtWidgets.QWidget(self.groupBox_DCscan)
        self.widget_7.setObjectName("widget_7")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget_7)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setHorizontalSpacing(9)
        self.gridLayout_7.setVerticalSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.but_dcscan = QtWidgets.QPushButton(self.widget_7)
        self.but_dcscan.setMinimumSize(QtCore.QSize(120, 0))
        self.but_dcscan.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.but_dcscan.setFont(font)
        self.but_dcscan.setMouseTracking(False)
        self.but_dcscan.setCheckable(False)
        self.but_dcscan.setAutoDefault(False)
        self.but_dcscan.setFlat(False)
        self.but_dcscan.setObjectName("but_dcscan")
        self.gridLayout_7.addWidget(self.but_dcscan, 0, 2, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.widget_7)
        self.progressBar.setMinimumSize(QtCore.QSize(250, 0))
        self.progressBar.setMaximumSize(QtCore.QSize(250, 16777215))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_7.addWidget(self.progressBar, 0, 0, 1, 2)
        self.checkBox = QtWidgets.QCheckBox(self.widget_7)
        self.checkBox.setEnabled(False)
        self.checkBox.setMinimumSize(QtCore.QSize(0, 25))
        self.checkBox.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_7.addWidget(self.checkBox, 1, 0, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.widget_7)
        self.checkBox_3.setEnabled(False)
        self.checkBox_3.setMinimumSize(QtCore.QSize(0, 25))
        self.checkBox_3.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_7.addWidget(self.checkBox_3, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.widget_7)
        self.gridLayout.addWidget(self.groupBox_DCscan, 1, 3, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_4.setSpacing(9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_8 = QtWidgets.QWidget(self.groupBox_3)
        self.widget_8.setObjectName("widget_8")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_8)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setHorizontalSpacing(10)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_10 = QtWidgets.QLabel(self.widget_8)
        self.label_10.setMinimumSize(QtCore.QSize(0, 15))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.widget_8)
        self.label_11.setMinimumSize(QtCore.QSize(0, 15))
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget_8)
        self.label_9.setMinimumSize(QtCore.QSize(0, 15))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 0, 2, 1, 1)
        self.spnbx_pzt_start = QtWidgets.QSpinBox(self.widget_8)
        self.spnbx_pzt_start.setMinimumSize(QtCore.QSize(87, 0))
        self.spnbx_pzt_start.setMaximumSize(QtCore.QSize(87, 16777215))
        self.spnbx_pzt_start.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_pzt_start.setFont(font)
        self.spnbx_pzt_start.setAlignment(QtCore.Qt.AlignCenter)
        self.spnbx_pzt_start.setObjectName("spnbx_pzt_start")
        self.gridLayout_5.addWidget(self.spnbx_pzt_start, 1, 0, 1, 1)
        self.spnbx_pzt_stop = QtWidgets.QSpinBox(self.widget_8)
        self.spnbx_pzt_stop.setMinimumSize(QtCore.QSize(87, 0))
        self.spnbx_pzt_stop.setMaximumSize(QtCore.QSize(87, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx_pzt_stop.setFont(font)
        self.spnbx_pzt_stop.setAlignment(QtCore.Qt.AlignCenter)
        self.spnbx_pzt_stop.setMaximum(100)
        self.spnbx_pzt_stop.setProperty("value", 100)
        self.spnbx_pzt_stop.setObjectName("spnbx_pzt_stop")
        self.gridLayout_5.addWidget(self.spnbx_pzt_stop, 1, 1, 1, 1)
        self.spinBox_pzt_freq = QtWidgets.QSpinBox(self.widget_8)
        self.spinBox_pzt_freq.setMinimumSize(QtCore.QSize(87, 0))
        self.spinBox_pzt_freq.setMaximumSize(QtCore.QSize(87, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBox_pzt_freq.setFont(font)
        self.spinBox_pzt_freq.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_pzt_freq.setPrefix("")
        self.spinBox_pzt_freq.setProperty("value", 10)
        self.spinBox_pzt_freq.setObjectName("spinBox_pzt_freq")
        self.gridLayout_5.addWidget(self.spinBox_pzt_freq, 1, 2, 1, 1)
        self.verticalLayout_4.addWidget(self.widget_8)
        self.label_13 = QtWidgets.QLabel(self.groupBox_3)
        self.label_13.setMinimumSize(QtCore.QSize(0, 15))
        self.label_13.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.verticalLayout_4.addWidget(self.label_13)
        self.widget_10 = QtWidgets.QWidget(self.groupBox_3)
        self.widget_10.setObjectName("widget_10")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget_10)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setHorizontalSpacing(10)
        self.gridLayout_8.setVerticalSpacing(0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_12 = QtWidgets.QLabel(self.widget_10)
        self.label_12.setMinimumSize(QtCore.QSize(87, 0))
        self.label_12.setMaximumSize(QtCore.QSize(87, 16777215))
        self.label_12.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_8.addWidget(self.label_12, 0, 0, 1, 1)
        self.but_pztscan = QtWidgets.QPushButton(self.widget_10)
        self.but_pztscan.setMinimumSize(QtCore.QSize(87, 0))
        self.but_pztscan.setMaximumSize(QtCore.QSize(87, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.but_pztscan.setFont(font)
        self.but_pztscan.setCheckable(False)
        self.but_pztscan.setChecked(False)
        self.but_pztscan.setAutoRepeat(False)
        self.but_pztscan.setObjectName("but_pztscan")
        self.gridLayout_8.addWidget(self.but_pztscan, 0, 2, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.widget_10)
        self.comboBox.setMinimumSize(QtCore.QSize(87, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(87, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_8.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.widget_10)
        self.label_14.setMinimumSize(QtCore.QSize(0, 25))
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")
        self.gridLayout_8.addWidget(self.label_14, 1, 0, 1, 1)
        self.comboBox.raise_()
        self.label_12.raise_()
        self.but_pztscan.raise_()
        self.label_14.raise_()
        self.verticalLayout_4.addWidget(self.widget_10)
        self.gridLayout.addWidget(self.groupBox_3, 1, 4, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        self.widget_23 = QtWidgets.QWidget(self.centralwidget)
        self.widget_23.setMinimumSize(QtCore.QSize(0, 580))
        self.widget_23.setObjectName("widget_23")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.widget_23)
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.widget_2 = QtWidgets.QWidget(self.widget_23)
        self.widget_2.setStyleSheet("")
        self.widget_2.setObjectName("widget_2")
        self.mplvl = QtWidgets.QVBoxLayout(self.widget_2)
        self.mplvl.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.mplvl.setContentsMargins(0, 0, 12, 0)
        self.mplvl.setSpacing(6)
        self.mplvl.setObjectName("mplvl")
        self.horizontalLayout_20.addWidget(self.widget_2)
        self.widget_5 = QtWidgets.QWidget(self.widget_23)
        self.widget_5.setMinimumSize(QtCore.QSize(0, 550))
        self.widget_5.setMaximumSize(QtCore.QSize(250, 16777215))
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_15.setContentsMargins(0, 15, 0, 15)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.groupBox_8 = QtWidgets.QGroupBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy)
        self.groupBox_8.setMinimumSize(QtCore.QSize(0, 110))
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_12.setContentsMargins(-1, 9, -1, 9)
        self.gridLayout_12.setSpacing(9)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.comboBox_SelectLine = QtWidgets.QComboBox(self.groupBox_8)
        self.comboBox_SelectLine.setMinimumSize(QtCore.QSize(87, 0))
        self.comboBox_SelectLine.setMaximumSize(QtCore.QSize(85, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_SelectLine.setFont(font)
        self.comboBox_SelectLine.setObjectName("comboBox_SelectLine")
        self.comboBox_SelectLine.addItem("")
        self.comboBox_SelectLine.addItem("")
        self.gridLayout_12.addWidget(self.comboBox_SelectLine, 0, 3, 1, 1)
        self.button_DataTip = QtWidgets.QPushButton(self.groupBox_8)
        self.button_DataTip.setMaximumSize(QtCore.QSize(110, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_DataTip.setFont(font)
        self.button_DataTip.setObjectName("button_DataTip")
        self.gridLayout_12.addWidget(self.button_DataTip, 0, 2, 1, 1)
        self.spnbx__downsample = QtWidgets.QSpinBox(self.groupBox_8)
        self.spnbx__downsample.setMinimumSize(QtCore.QSize(87, 0))
        self.spnbx__downsample.setMaximumSize(QtCore.QSize(85, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbx__downsample.setFont(font)
        self.spnbx__downsample.setMinimum(1)
        self.spnbx__downsample.setMaximum(10000)
        self.spnbx__downsample.setProperty("value", 10)
        self.spnbx__downsample.setObjectName("spnbx__downsample")
        self.gridLayout_12.addWidget(self.spnbx__downsample, 1, 3, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_8)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_12.addWidget(self.pushButton_3, 1, 2, 1, 1)
        self.verticalLayout_15.addWidget(self.groupBox_8)
        self.groupBox_9 = QtWidgets.QGroupBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy)
        self.groupBox_9.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_9.setObjectName("groupBox_9")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.groupBox_9)
        self.verticalLayout_16.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_16.setSpacing(9)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.widget_24 = QtWidgets.QWidget(self.groupBox_9)
        self.widget_24.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_24.setMaximumSize(QtCore.QSize(20000, 16777215))
        self.widget_24.setObjectName("widget_24")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_24)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.but_setdir = QtWidgets.QPushButton(self.widget_24)
        self.but_setdir.setMinimumSize(QtCore.QSize(40, 0))
        self.but_setdir.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.but_setdir.setFont(font)
        self.but_setdir.setObjectName("but_setdir")
        self.gridLayout_3.addWidget(self.but_setdir, 4, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.widget_24)
        self.label_17.setMinimumSize(QtCore.QSize(50, 0))
        self.label_17.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 5, 0, 1, 1)
        self.comboBox_Extension = QtWidgets.QComboBox(self.widget_24)
        self.comboBox_Extension.setMinimumSize(QtCore.QSize(87, 0))
        self.comboBox_Extension.setMaximumSize(QtCore.QSize(175, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_Extension.setFont(font)
        self.comboBox_Extension.setFrame(False)
        self.comboBox_Extension.setObjectName("comboBox_Extension")
        self.comboBox_Extension.addItem("")
        self.comboBox_Extension.addItem("")
        self.comboBox_Extension.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_Extension, 6, 1, 1, 1)
        self.text_File = QtWidgets.QLineEdit(self.widget_24)
        self.text_File.setMinimumSize(QtCore.QSize(160, 0))
        self.text_File.setMaximumSize(QtCore.QSize(175, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.text_File.setFont(font)
        self.text_File.setObjectName("text_File")
        self.gridLayout_3.addWidget(self.text_File, 5, 1, 1, 1)
        self.text_Dir = QtWidgets.QLineEdit(self.widget_24)
        self.text_Dir.setMinimumSize(QtCore.QSize(160, 0))
        self.text_Dir.setMaximumSize(QtCore.QSize(175, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.text_Dir.setFont(font)
        self.text_Dir.setObjectName("text_Dir")
        self.gridLayout_3.addWidget(self.text_Dir, 4, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.widget_24)
        self.label_16.setMinimumSize(QtCore.QSize(50, 0))
        self.label_16.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 6, 0, 1, 1)
        self.verticalLayout_16.addWidget(self.widget_24)
        self.but_savedata = QtWidgets.QPushButton(self.groupBox_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.but_savedata.setFont(font)
        self.but_savedata.setObjectName("but_savedata")
        self.verticalLayout_16.addWidget(self.but_savedata)
        self.verticalLayout_16.setStretch(0, 1)
        self.verticalLayout_16.setStretch(1, 1)
        self.verticalLayout_15.addWidget(self.groupBox_9)
        self.groupBox_7test = QtWidgets.QGroupBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_7test.sizePolicy().hasHeightForWidth())
        self.groupBox_7test.setSizePolicy(sizePolicy)
        self.groupBox_7test.setMinimumSize(QtCore.QSize(0, 250))
        self.groupBox_7test.setObjectName("groupBox_7test")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_7test)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox_7test)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout_7.addWidget(self.checkBox_5)
        self.widgettest = QtWidgets.QWidget(self.groupBox_7test)
        self.widgettest.setEnabled(False)
        self.widgettest.setObjectName("widgettest")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widgettest)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_24 = QtWidgets.QLabel(self.widgettest)
        self.label_24.setEnabled(False)
        self.label_24.setObjectName("label_24")
        self.verticalLayout_9.addWidget(self.label_24)
        self.checkBox_6 = QtWidgets.QCheckBox(self.widgettest)
        self.checkBox_6.setEnabled(False)
        self.checkBox_6.setObjectName("checkBox_6")
        self.verticalLayout_9.addWidget(self.checkBox_6)
        self.widgettesttest = QtWidgets.QWidget(self.widgettest)
        self.widgettesttest.setEnabled(False)
        self.widgettesttest.setObjectName("widgettesttest")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widgettesttest)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_23 = QtWidgets.QLabel(self.widgettesttest)
        self.label_23.setEnabled(False)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_2.addWidget(self.label_23)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.widgettesttest)
        self.doubleSpinBox.setEnabled(False)
        self.doubleSpinBox.setMinimumSize(QtCore.QSize(87, 0))
        self.doubleSpinBox.setMaximumSize(QtCore.QSize(110, 16777215))
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout_2.addWidget(self.doubleSpinBox)
        self.verticalLayout_9.addWidget(self.widgettesttest)
        self.widgettest445 = QtWidgets.QWidget(self.widgettest)
        self.widgettest445.setEnabled(False)
        self.widgettest445.setObjectName("widgettest445")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widgettest445)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.checkBox_7 = QtWidgets.QCheckBox(self.widgettest445)
        self.checkBox_7.setEnabled(False)
        self.checkBox_7.setObjectName("checkBox_7")
        self.verticalLayout_10.addWidget(self.checkBox_7)
        self.widget_2test = QtWidgets.QWidget(self.widgettest445)
        self.widget_2test.setEnabled(False)
        self.widget_2test.setObjectName("widget_2test")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_2test)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_27 = QtWidgets.QLabel(self.widget_2test)
        self.label_27.setEnabled(False)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_3.addWidget(self.label_27)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget_2test)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(110, 0))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(110, 16777215))
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_3.addWidget(self.lineEdit_3)
        self.verticalLayout_10.addWidget(self.widget_2test)
        self.verticalLayout_9.addWidget(self.widgettest445)
        self.verticalLayout_7.addWidget(self.widgettest)
        self.verticalLayout_15.addWidget(self.groupBox_7test)
        self.horizontalLayout_20.addWidget(self.widget_5)
        self.verticalLayout.addWidget(self.widget_23)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1073, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionReport_Problem = QtWidgets.QAction(MainWindow)
        self.actionReport_Problem.setObjectName("actionReport_Problem")
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionReport_Problem)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.checkBox_2.clicked['bool'].connect(self.label_8.setEnabled)
        self.checkBox_2.clicked['bool'].connect(self.lineEdit.setEnabled)
        self.checkBox_2.clicked['bool'].connect(self.pushButton_4.setEnabled)
        self.checkBox_2.clicked['bool'].connect(self.label_15.setEnabled)
        self.checkBox_2.clicked['bool'].connect(self.lineEdit_2.setEnabled)
        self.checkBox_2.clicked['bool'].connect(self.checkBox.setEnabled)
        self.checkBox_4.clicked['bool'].connect(self.comboBox_5.setEnabled)
        self.checkBox_4.clicked['bool'].connect(self.lineEdit_4.setEnabled)
        self.checkBox_4.clicked['bool'].connect(self.label_25.setEnabled)
        self.checkBox_4.clicked['bool'].connect(self.lbl_wavemeterlbd.setEnabled)
        self.checkBox_4.clicked['bool'].connect(self.checkBox_3.setEnabled)
        self.checkBox_4.clicked['bool'].connect(self.pushButton_5.setEnabled)
        self.checkBox_5.clicked['bool'].connect(self.widgettest.setEnabled)
        self.checkBox_5.clicked['bool'].connect(self.label_24.setEnabled)
        self.checkBox_5.clicked['bool'].connect(self.checkBox_6.setEnabled)
        self.checkBox_6.clicked['bool'].connect(self.widgettesttest.setEnabled)
        self.checkBox_6.clicked['bool'].connect(self.doubleSpinBox.setEnabled)
        self.checkBox_6.clicked['bool'].connect(self.label_23.setEnabled)
        self.checkBox_6.clicked['bool'].connect(self.widgettesttest.setEnabled)
        self.checkBox_6.clicked['bool'].connect(self.widgettest445.setEnabled)
        self.checkBox_6.clicked['bool'].connect(self.checkBox_7.setEnabled)
        self.checkBox_7.clicked['bool'].connect(self.widget_2test.setEnabled)
        self.checkBox_7.clicked['bool'].connect(self.label_27.setEnabled)
        self.checkBox_7.clicked['bool'].connect(self.lineEdit_3.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.spnbx_lbd, self.spnbx_I)
        MainWindow.setTabOrder(self.spnbx_I, self.spnbx_pzt)
        MainWindow.setTabOrder(self.spnbx_pzt, self.spnbx_lbd_start)
        MainWindow.setTabOrder(self.spnbx_lbd_start, self.spnbx_lbd_stop)
        MainWindow.setTabOrder(self.spnbx_lbd_stop, self.spnbx_speed)
        MainWindow.setTabOrder(self.spnbx_speed, self.checkBox)
        MainWindow.setTabOrder(self.checkBox, self.checkBox_3)
        MainWindow.setTabOrder(self.checkBox_3, self.but_dcscan)
        MainWindow.setTabOrder(self.but_dcscan, self.spnbx_pzt_start)
        MainWindow.setTabOrder(self.spnbx_pzt_start, self.spnbx_pzt_stop)
        MainWindow.setTabOrder(self.spnbx_pzt_stop, self.spinBox_pzt_freq)
        MainWindow.setTabOrder(self.spinBox_pzt_freq, self.comboBox_SelectLine)
        MainWindow.setTabOrder(self.comboBox_SelectLine, self.button_DataTip)
        MainWindow.setTabOrder(self.button_DataTip, self.but_setdir)
        MainWindow.setTabOrder(self.but_setdir, self.comboBox_Extension)
        MainWindow.setTabOrder(self.comboBox_Extension, self.text_File)
        MainWindow.setTabOrder(self.text_File, self.text_Dir)
        MainWindow.setTabOrder(self.text_Dir, self.but_savedata)
        MainWindow.setTabOrder(self.but_savedata, self.spnbx__downsample)
        MainWindow.setTabOrder(self.spnbx__downsample, self.but_pztscan)
        MainWindow.setTabOrder(self.but_pztscan, self.comboBox)
        MainWindow.setTabOrder(self.comboBox, self.lineEdit)
        MainWindow.setTabOrder(self.lineEdit, self.lineEdit_2)
        MainWindow.setTabOrder(self.lineEdit_2, self.slide_pzt)
        MainWindow.setTabOrder(self.slide_pzt, self.comboBox_2)
        MainWindow.setTabOrder(self.comboBox_2, self.comboBox_3)
        MainWindow.setTabOrder(self.comboBox_3, self.comboBox_4)
        MainWindow.setTabOrder(self.comboBox_4, self.spnbx_daq_Vmin)
        MainWindow.setTabOrder(self.spnbx_daq_Vmin, self.spnbx_daq_Vmax)
        MainWindow.setTabOrder(self.spnbx_daq_Vmax, self.comboBox_5)
        MainWindow.setTabOrder(self.comboBox_5, self.lineEdit_4)
        MainWindow.setTabOrder(self.lineEdit_4, self.pushButton_3)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Transmission Measurement"))
        self.pushButton_2.setText(_translate("MainWindow", "Output"))
        self.but_connect.setText(_translate("MainWindow", "Connect"))
        self.comboBox_6.setItemText(0, _translate("MainWindow", "NF6700"))
        self.groupBox_5.setTitle(_translate("MainWindow", "DAQ"))
        self.label_18.setText(_translate("MainWindow", "DAQ Device"))
        self.label_19.setText(_translate("MainWindow", "T. Channel"))
        self.label_20.setText(_translate("MainWindow", "MZ. Channel"))
        self.label_21.setText(_translate("MainWindow", "V<sub>min</sub>"))
        self.label_22.setText(_translate("MainWindow", "V<sub>max</sub>"))
        self.comboBox_8.setItemText(0, _translate("MainWindow", "ai1"))
        self.comboBox_8.setItemText(1, _translate("MainWindow", "ai2"))
        self.comboBox_8.setItemText(2, _translate("MainWindow", "ai3"))
        self.comboBox_8.setItemText(3, _translate("MainWindow", "ai4"))
        self.comboBox_8.setItemText(4, _translate("MainWindow", "ai5"))
        self.comboBox_8.setItemText(5, _translate("MainWindow", "ai6"))
        self.label_28.setText(_translate("MainWindow", "Probe Piezo Channel"))
        self.groupBox.setTitle(_translate("MainWindow", "Static Parameters"))
        self.label_2.setText(_translate("MainWindow", "Current"))
        self.label.setText(_translate("MainWindow", "Wavelength"))
        self.spnbx_I.setSuffix(_translate("MainWindow", " A"))
        self.spnbx_lbd.setSuffix(_translate("MainWindow", " nm"))
        self.label_3.setText(_translate("MainWindow", "Piezo"))
        self.spnbx_pzt.setSuffix(_translate("MainWindow", " %"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Power Detectors"))
        self.pushButton_4.setText(_translate("MainWindow", "Update"))
        self.checkBox_2.setText(_translate("MainWindow", "Connect"))
        self.label_15.setText(_translate("MainWindow", "P<sub>out</sub>"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p>P<span style=\" vertical-align:sub;\">in</span></p></body></html>"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Wavemeter"))
        self.lbl_wavemeterlbd.setText(_translate("MainWindow", "<html><head/><body><p>λ</p></body></html>"))
        self.label_25.setText(_translate("MainWindow", "<html><head/><body><p>Chanel</p></body></html>"))
        self.checkBox_4.setText(_translate("MainWindow", "Connect"))
        self.pushButton_5.setText(_translate("MainWindow", "Update"))
        self.groupBox_DCscan.setTitle(_translate("MainWindow", "DC Scan Parameters"))
        self.label_4.setText(_translate("MainWindow", "λ<sub>start</sub>"))
        self.label_5.setText(_translate("MainWindow", "λ<sub>stop</sub>"))
        self.label_6.setText(_translate("MainWindow", "Speed "))
        self.spnbx_lbd_start.setSuffix(_translate("MainWindow", " nm"))
        self.spnbx_lbd_stop.setSuffix(_translate("MainWindow", " nm"))
        self.spnbx_speed.setSuffix(_translate("MainWindow", " nm/s"))
        self.but_dcscan.setText(_translate("MainWindow", "Scan"))
        self.checkBox.setText(_translate("MainWindow", "3 pts Transmision"))
        self.checkBox_3.setText(_translate("MainWindow", "Calib λ"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Piezo Scan Parameters"))
        self.label_10.setText(_translate("MainWindow", "Min"))
        self.label_11.setText(_translate("MainWindow", "Max"))
        self.label_9.setText(_translate("MainWindow", "Freq"))
        self.spnbx_pzt_start.setSuffix(_translate("MainWindow", " %"))
        self.spnbx_pzt_stop.setSuffix(_translate("MainWindow", " %"))
        self.spinBox_pzt_freq.setSuffix(_translate("MainWindow", " Hz"))
        self.label_12.setText(_translate("MainWindow", "Channel"))
        self.but_pztscan.setText(_translate("MainWindow", "Pzt Scan"))
        self.comboBox.setItemText(0, _translate("MainWindow", "ao1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "ao2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "ao3"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Plot Settings"))
        self.comboBox_SelectLine.setItemText(0, _translate("MainWindow", "Line 1"))
        self.comboBox_SelectLine.setItemText(1, _translate("MainWindow", "Line 2"))
        self.button_DataTip.setText(_translate("MainWindow", "Show Data Tip"))
        self.pushButton_3.setText(_translate("MainWindow", "DownSample"))
        self.groupBox_9.setTitle(_translate("MainWindow", "Save Settings"))
        self.but_setdir.setText(_translate("MainWindow", "Dir"))
        self.label_17.setText(_translate("MainWindow", "Name"))
        self.comboBox_Extension.setItemText(0, _translate("MainWindow", ".mat"))
        self.comboBox_Extension.setItemText(1, _translate("MainWindow", ".dill"))
        self.comboBox_Extension.setItemText(2, _translate("MainWindow", "all"))
        self.label_16.setText(_translate("MainWindow", "Format"))
        self.but_savedata.setText(_translate("MainWindow", "Save Data"))
        self.groupBox_7test.setTitle(_translate("MainWindow", "Post-Processing"))
        self.checkBox_5.setText(_translate("MainWindow", "True λ With MZ and λmetter"))
        self.label_24.setText(_translate("MainWindow", "Experimental:"))
        self.checkBox_6.setText(_translate("MainWindow", "Find Resonances"))
        self.label_23.setText(_translate("MainWindow", "Targeted FSR"))
        self.doubleSpinBox.setSuffix(_translate("MainWindow", " GHz"))
        self.checkBox_7.setText(_translate("MainWindow", "Fit Q"))
        self.label_27.setText(_translate("MainWindow", "Average Q:"))
        self.lineEdit_3.setText(_translate("MainWindow", "0"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionReport_Problem.setText(_translate("MainWindow", "Report Problem"))

import style_rc
