# This Python file uses the following encoding: utf-8
import sys

import PyQt6.QtWidgets
from PyQt6.QtGui import QPixmap, QImage

from dataset.dataset import DatasetType, Dataset
from ui import ui

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

import logging

from dataset.table import TableView
from ui.imagegallery import ImageGallery
from ui.imagelabel import ImageLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('form.ui', self)
        logging.basicConfig(level=logging.DEBUG)
        self.dataset = Dataset(DatasetType.KITTI_IMG, '/home/biblbrox/autonet/test_kitti/')
        self.images, self.labels = self.dataset.get_labeled()

        self.init_dataset_overview()
        self.init_diagram_cell()
        self.init_info_cell()
        self.init_table_cell()

    def init_diagram_cell(self):
        classes = self.dataset.classes_dict
        diagram = ui.make_diagram(self, classes)
        self.gridLayout.addWidget(diagram, 0, 0)

    def init_info_cell(self):
        dataset_info = PyQt6.QtWidgets.QLabel(self)
        classes = self.dataset.classes_dict
        dataset_info.setText(
            f"Classes count: {len(classes.keys())}\n Images count: {len(self.images)}\n Labeled: {len(self.labels)}")
        self.gridLayout.addWidget(dataset_info, 0, 1)

    def init_table_cell(self):
        classes = self.dataset.classes_dict
        data = {'Classes': classes.keys(),
                'Images': [1, 2]
                }

        table = TableView(data, 3, 4)
        self.gridLayout.addWidget(table, 1, 0)

    def init_dataset_overview(self):
        image_gallery = ImageGallery(self.images, self)
        self.scrollAreaWidgetContents.setLayout(image_gallery)


if __name__ == "__main__":
    app = QApplication([])
    with open("./styles/styles.qss") as styles:
        app.setStyleSheet("".join(styles.readlines()))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
