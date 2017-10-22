#TODO, define actions of buttons, fix the table
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QTableWidget, QTableWidgetItem, QTreeView, QTreeWidgetItem, QTreeWidget,)

from PyQt5.Qt import (QAbstractTableModel, Qt, QAbstractListModel, QWidget,
        pyqtSignal, QVBoxLayout, QDialogButtonBox, QFrame, QLabel, QIcon)

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

        self.resize(400, 250)
        self.setWindowTitle("Own Differential Backup")

    def create_table(self):
        self.table = QGroupBox("")
        
        layout = QGridLayout()
        data = {'Data folder':['1','2','3','3'],  #change the data
                'Backup folder':['4','5','6','2']}

        table = QTableWidget(self)
        table.setRowCount(2) #create variable here for number of rows
        table.setColumnCount(2)

        #Enter data onto Table
        horHeaders = []
        for n, key in enumerate(sorted(data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                newitem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled) #adds checkbox
                newitem.setCheckState(Qt.Unchecked)
                table.setItem(m, n, newitem)
        #Add Header
        table.setHorizontalHeaderLabels(horHeaders)        

        #Adjust size of Table
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        layout.addWidget(table, 0,0)   

        self.table.setLayout(layout)

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