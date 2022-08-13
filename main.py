# This Python file uses the following encoding: utf-8
import os.path
import sys

import PyQt6.QtWidgets
from PyQt6.QtGui import QPixmap, QImage

from dataset.dataset import DatasetType, Dataset
from translate import tr
from ui import ui

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic, QtCore

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
        self.image_classes = []
        for i in range(len(self.images)):
            self.image_classes.append('ImageLabelLabeled' if i < len(self.labels) else 'ImageLabelUnlabeled')

        self.init_dataset_overview()
        self.init_diagram_cell()
        self.init_info_cell()
        #self.init_table_cell()

    def init_diagram_cell(self):
        classes = self.dataset.classes_dict
        diagram = ui.make_diagram(self, classes)
        diagram.set_window_title(tr("Classes distribution"))
        self.gridLayout.addWidget(diagram, 0, 0)

    def init_info_cell(self):
        dataset_info = PyQt6.QtWidgets.QLabel(self)
        classes = self.dataset.classes_dict
        images_info = f"Images count: {len(self.images)}"
        labels_info = f"Labels count: {len(self.labels)}"
        obj_count = 0
        for obj in self.dataset.get_objects_gen():
            obj_count += len(obj)
        objects_info = f"Total number of objects (instances): {obj_count}"
        dataset_info.setText(f"{images_info}\n{labels_info}\n{objects_info}")
        dataset_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft and QtCore.Qt.AlignmentFlag.AlignTop)
        self.gridLayout.addWidget(dataset_info, 0, 1)

    def init_table_cell(self):
        classes = self.dataset.classes_dict
        data = {'Classes': classes.keys(),
                'Images': [1, 2]
                }

        table = TableView(data, 3, 4)
        self.gridLayout.addWidget(table, 1, 0)

    def init_dataset_overview(self):
        image_gallery = ImageGallery(self.images, self.image_classes, self)
        self.scrollAreaWidgetContents.setLayout(image_gallery)


if __name__ == "__main__":
    logging.basicConfig(
        # filename='HISTORYlistener.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    app = QApplication([])
    with open("./styles/styles.qss") as styles:
        app.setStyleSheet("".join(styles.readlines()))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
