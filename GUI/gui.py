#TODO, define actions of buttons, fix the table
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QTableWidget, QTableWidgetItem, QTreeView, QTreeWidgetItem, QTreeWidget, QTableView)

from PyQt5.Qt import (QAbstractTableModel, Qt, QAbstractListModel, QWidget,
        pyqtSignal, QVBoxLayout, QDialogButtonBox, QFrame, QLabel, QIcon, QVariant)

class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()

        self.create_table()
        self.horizontal_button()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.hlayout)
        mainLayout.addWidget(self.table)        
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.resize(600, 250)
        self.setWindowTitle("Own Differential Backup")

    def create_table(self):
        #tablemodel = Model(self)
        #tablemodel = QAbstractTableModel
        self.table = QTableView()
        #self.table.setModel(tablemodel)

        layout = QGridLayout()

        data_folder = {1: "/mnt/SHARED_DATA/Repository/odb/data", 2: "Algo", 3: "Algo dadada"}
        backup_folder = {1: "/mnt/SHARED_DATA/Repository/odb/backup", 2: "Algo mes", 3: "Algo mes dadaada"}

        table = QTableWidget(self)
        table.setRowCount(len(data_folder)) #create variable here for number of rows
        table.setColumnCount(3)

        #Enter data onto Table
        horHeaders = ["Backup folder", "Data folder", "" ]

        row = 0
        for n, key in enumerate(backup_folder):
            n = 0
            newbackupitem = QTableWidgetItem(backup_folder[key])
            newdataitem = QTableWidgetItem(data_folder[key])

            newcheckbox = QTableWidgetItem("")
            newcheckbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled) #adds checkbox
            newcheckbox.setCheckState(Qt.Unchecked)
            

            table.setItem(row, n, newbackupitem)
            table.setItem(row, n+1, newdataitem)
            table.setItem(row, n+2, newcheckbox)
            row += 1

        table.itemClicked.connect(self.handleItemClicked)
        #Add Header
        table.setHorizontalHeaderLabels(horHeaders)        

        #Adjust size of Table
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setSelectionBehavior(QTableView.SelectRows)
        
        layout.addWidget(table, 0,0)   

        self.table.setLayout(layout)
        self._list = []

    def handleItemClicked(self, item):
        
        rows = self.table.selectionModel().selectedIndexes()
        for row in rows:
            cellContent = row.data()
            print(cellContent)

    def horizontal_button(self):
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


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
