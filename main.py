import os
from PySide2.QtWidgets import (QApplication, QDialog, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog,
    QLabel, QTableView, QCheckBox, QHeaderView)
from models import UnitTableModel

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

            
    def select_folder(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec_():
            filenames = dialog.selectedFiles()
            self.folder_address_input.setText(filenames[0])
    
    def compress_files(self):
        files_dir = self.folder_address_input.text()
        print("Compressing files on {}".format(files_dir))
        print("Files compressed")
    
    def upload_files(self):
        print("Uploading files to server")
        print("Files uploaded")

    def update(self):
        print("Updating files")
        self.compress_files()
        self.upload_files()
        print("Update completed")

    # def update_model(self, datalist, header):
    #     self.table_model2 = MyTableModel(self, dataList, header)
    #     self.table_view.setModel(self.table_model2)
    #     self.table_view.update()


app = QApplication([])

header = ['No Servidor', 'Arquivo encontrado', 'Confere?']
datalist = [
    ('Camara Municipal do Rio de Janeiro', 
        'Câmara Municipal', 
        QCheckBox()
    ),
    ('Secretaria Municipal de Saude', 
        'Secretaria Municipal de Sa&de', 
        QCheckBox()
    ),
    ('Secretaria Municipal de Educacao', 
        'Secretaria Municipal de EducasSáum', 
        QCheckBox()
    ),
]
form = MainForm(datalist, header)
form.show()
app.exec_()
