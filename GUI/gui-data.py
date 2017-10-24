from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QTableWidget, QTableWidgetItem, QTreeView, QTreeWidgetItem, QTreeWidget, QTableView)

from PyQt5.Qt import (QAbstractTableModel, Qt, QAbstractListModel, QWidget,
        pyqtSignal, QVBoxLayout, QDialogButtonBox, QFrame, QLabel, QIcon, QVariant)
import sys

class Model(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.items = ['Row0_Column0','Row0_Column1','Row0_Column2']

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, parent):
        return 1      
    def columnCount(self, parent):
        return len(self.items)  

    def data(self, index, role):
        if not index.isValid(): return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()

        column=index.column()
        if column<len(self.items):
            return QVariant(self.items[column])
        else:
            return QVariant()

class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        tablemodel=Model(self)               

        self.tableview=QTableView() 
        self.tableview.setModel(tablemodel)
        self.tableview.clicked.connect(self.viewClicked)

        self.tableview.setSelectionBehavior(QTableView.SelectRows)
        self.tableview.clicked.connect(self.showSelection)

        layout = QHBoxLayout(self)
        layout.addWidget(self.tableview)

        self.setLayout(layout)

    def showSelection(self, item):
        rows = self.tableview.selectionModel().selectedIndexes()
        for row in rows:
            cellContent = row.data()
            print(cellContent)
        #print(rows)
        #print(cellContent)

    def viewClicked(self, clickedIndex):
        lists = []
        #print(row)
        model=clickedIndex.model()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())