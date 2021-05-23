import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtWidgets import QHeaderView


class EventTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None):
        super(EventTableModel, self).__init__()

        self.column_names = []

        if data is None:
            self._data = []
        else:
            self._data = data

    def data(self, index, role=Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not
            returning data, return None (PySide equivalent of QT's
            "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._data):
            return None

        if role == Qt.DisplayRole:
            return self._data[index.row()][self.column_names[index.column()]]

    def rowCount(self, index=QModelIndex()):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self.column_names)

    def addColumn(self, name):
        new_column = self.columnCount()
        self.beginInsertColumns(QModelIndex(), new_column, new_column)
        for i in range(self.rowCount()):
            self._data[i][name] = ""

        self.endInsertColumns()
        self.column_names.append(name)

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)

        for row in range(rows):
            empty_row = dict()
            for col in self.column_names:
                empty_row[col] = ""
            self._data.insert(position + row, empty_row)

        self.endInsertRows()
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section < len(self.column_names):
                return self.column_names[section]
            else:
                return None

    def removeRows(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)

        del self._data[position:position + rows]

        self.endRemoveRows()
        return True

    def setData(self, index, value, role=Qt.EditRole):
        """ Adjust the data (set it to <value>) depending on the given
            index and role.
        """

        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self._data):
            if index.column() < len(self.column_names):
                current_dict = self._data[index.row()]
                current_dict.update({self.column_names[index.column()]: value})
            else:
                return False

            self.dataChanged.emit(index, index)
            return True

        return False


