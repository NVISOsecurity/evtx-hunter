import sys

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QFile, QIODevice
from PySide2.QtUiTools import QUiLoader

from models.event_table_model import EventTableModel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        ui_file_name = "resources/ui/main_window.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        if not self.window:
            print(loader.errorString())
            sys.exit(-1)

        # EventTable
        self.eventTableModel = EventTableModel()
        self.window.eventTableView.setModel(self.eventTableModel)

        # FieldList
        self.fieldListModel = QtGui.QStandardItemModel()
        self.window.fieldListView.setModel(self.fieldListModel)
        #self.fieldListModel.itemChanged.connect(self.handleItemChanged)

        # Window
        self.setWindowTitle("evtx-hunter")
        self.setCentralWidget(self.window)
        self.showMaximized()

