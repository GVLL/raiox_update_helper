import os
import data
from PySide2.QtWidgets import (QApplication, QDialog, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog,
    QLabel, QTableView, QCheckBox, QHeaderView)
from PySide2.QtCore import QThread
from models import UnitTableModel
from utils import nearest, compressfile, Status, upload_sheet


HEADER = ['No Servidor', 'Arquivo encontrado', 'Confere?']

class MainForm(QDialog):
    def __init__(self, datalist, header, parent=None):
            super(MainForm, self).__init__(parent)
            self.setWindowTitle("Raio-X do Orçamento Helper")
            self.setMinimumSize(800, 600)
            self.year_label = QLabel("Ano")
            self.year_input = QLineEdit("2019")
            

            self.selection_button = QPushButton("Selecionar pasta")
            self.selection_button.clicked.connect(self.select_folder)

            self.update_button = QPushButton("Atualizar Dados")
            self.update_button.clicked.connect(self.update)

            self.folder_address_input = QLineEdit(".")

            layout = QVBoxLayout()
            # layout.addWidget(self.year_label)
            layout.addWidget(self.year_input)
            
            hlayout = QHBoxLayout()
            hlayout.addWidget(self.selection_button)
            hlayout.addWidget(self.folder_address_input)
            layout.addLayout(hlayout)
            
            # tabela
            self.datalist = datalist
            self.table_model = UnitTableModel(self, datalist, header)
            self.table_view = QTableView()
            #self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
            # self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table_view.setModel(self.table_model)
            # bind cell click to a method reference
            # self.table_view.clicked.connect(self.showSelection)
            # self.table_view.clicked.connect(self.selectRow)
            # enable sorting
            # self.table_view.setSortingEnabled(True)
            self.resize_header()
            layout.addWidget(self.table_view)
            layout.addWidget(self.update_button)
            self.setLayout(layout)

    def resize_header(self):
        header = self.table_view.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def showSelection(self, item):
        cellContent = item.data()
        # print(cellContent)  # test
        sf = "You clicked on {}".format(cellContent)
        # display in title bar for convenience
        self.setWindowTitle(sf)

    def update_model(self, folder):
        filenames = os.listdir(folder)
        self.datalist = [(unit, nearest(unit, filenames), QCheckBox()) for unit in data.units]
        self.table_model = UnitTableModel(self, self.datalist, HEADER)
        self.table_view.setModel(self.table_model)
        self.table_view.update()
            
    def select_folder(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec_():
            selected_dir = dialog.selectedFiles()[0]
            self.folder_address_input.setText(selected_dir)
            self.update_model(selected_dir)
    
    def compress_files(self):
        files_dir = self.folder_address_input.text()
        for row in self.datalist:
            print("Compressing file {}".format(row[1]))
            compressfile(os.path.join(files_dir, row[1]), os.path.join(files_dir, row[0]))
    
    def upload_files(self):
        files_dir = self.folder_address_input.text()
        for count, row in enumerate(self.datalist):
            print("Uploading file {}".format(row[0]))
            # TODO: read year from UI (combobox?)
            upload_sheet(os.path.join(files_dir, row[0]), 2019)
            self.table_model.update_row_status(count, Status.SENT)
        print("Files uploaded")

    def update(self):
        print("Updating files")
        self.compress_files()
        self.upload_files()
        print("Update completed")


app = QApplication([])

header = ['No Servidor', 'Arquivo encontrado', 'Confere?']
fake_units = data.units
datalist = [(unit, "---", QCheckBox("!")) for unit in data.units]

form = MainForm(datalist, header)
form.show()
app.exec_()
