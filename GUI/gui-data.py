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
        self.data_folder = ["/mnt/SHARED_DATA/Repository/odb/data", "pene"]
        self.backup_folder = ["/mnt/SHARED_DATA/Repository/odb/backup"]
        #data_folder = {1: "/mnt/SHARED_DATA/Repository/odb/data", 2: "Algo", 3: "Algo dadada"}
        #backup_folder = {1: "/mnt/SHARED_DATA/Repository/odb/backup", 2: "Algo mes", 3: "Algo mes dadaada"}

    def rowCount(self, parent):
        return len(self.data_folder)      
    def columnCount(self, parent):
        return len(self.data_folder)  

    def data(self, index, role): #gotta modify this
        print(index)
        if not index.isValid(): return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()

        column=index.column()
        if column<len(self.data_folder):
            return QVariant(self.data_folder[column])
        else:
            return QVariant()

class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.resize(600, 250)
        self.setWindowTitle("Own Differential Backup")
       
       ### Buttons ###
        self.hlayout = QGroupBox("")
        layout = QGridLayout()
        self.sync = QPushButton('Synchronize')
        self.sync.setMaximumWidth(100)

        self.add = QPushButton('Add')
        self.add.setMaximumWidth(65)

        self.delete = QPushButton('Delete')
        self.delete.setMaximumWidth(65)

        layout.addWidget(self.sync, 0, 0, 0, 0)
        layout.addWidget(self.add, 0, 5, 4, 1)
        layout.addWidget(self.delete, 0, 6, 4, 1)

        self.hlayout.setLayout(layout)

        ### Table ###
        tablemodel=Model(self)               


        self.tableview=QTableView() 
        #self.tableview.setRowCount(len(data_folder))
        #self.tableview.setColumnCount(3)
        self.tableview.setModel(tablemodel)
        self.tableview.clicked.connect(self.viewClicked)

        self.tableview.setSelectionBehavior(QTableView.SelectRows)
        self.tableview.clicked.connect(self.showSelection)

        ### Main Layout ###
        layout = QVBoxLayout(self)
        layout.addWidget(self.hlayout)        
        layout.addWidget(self.tableview)

        self.setLayout(layout)

    def showSelection(self, item):
        rows = self.tableview.selectionModel().selectedIndexes()
        for row in rows:
            cellContent = row.data()
            print(cellContent)

    def viewClicked(self, clickedIndex):
        lists = []
        model=clickedIndex.model()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())