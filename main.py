# This Python file uses the following encoding: utf-8
import os.path
import sys

import PyQt6.QtWidgets
from PyQt6.QtGui import QPixmap, QImage, QFont

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

        self.actionOpen_dataset.triggered.connect(self.on_action_open_dataset)

        self.image_label = dict(zip(self.images, self.labels))
        self.init_dataset_overview()
        self.init_diagram_cell()
        self.init_info_cell()
        # self.init_table_cell()

    def on_action_open_dataset(self):
        dataset_path = PyQt6.QtWidgets.QFileDialog.getExistingDirectory(self, tr("Select dataset root folder"))
        #dataset_type =

    def update_info(self):
        self.init_info_cell()
        self.init_dataset_overview()
        self.init_diagram_cell()

    def init_diagram_cell(self):
        classes = self.dataset.classes_dict
        diagram = ui.make_diagram(self, classes)
        diagram.set_window_title(tr("Classes distribution"))
        self.gridLayout.addWidget(diagram, 0, 0)

    def init_info_cell(self):
        dataset_info = PyQt6.QtWidgets.QLabel(self)
        images_info = f"Images count: {len(self.images)}"
        labels_info = f"Labels count: {len(self.labels)}"
        obj_count = sum(len(obj) for obj in self.dataset.get_objects_gen())
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
        image_gallery.tip_signal.connect(self.on_dataset_overview_tip)
        self.scrollAreaWidgetContents.setLayout(image_gallery)

    def on_dataset_overview_tip(self, pos, image_file):
        if image_file not in self.image_label.keys():
            return

        label_file = self.image_label[image_file]
        with open(label_file) as f:
            label_info = f.readlines()

        font = QFont()
        font.setFamily("Serif")
        PyQt6.QtWidgets.QToolTip.setFont(font)
        PyQt6.QtWidgets.QToolTip.showText(pos, "".join(label_info))


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
