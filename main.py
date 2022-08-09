# This Python file uses the following encoding: utf-8
import sys
from collections import Counter

import PyQt6.QtWidgets

from dataset.dataset import DatasetType, Dataset
from PyQt6.QtCore import QFile, QTextStream
import os
# import styles.breeze_resources
from dataset import ui

from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt6.QtCore import QFile, QIODevice
from PyQt6 import uic

import logging

from dataset.table import TableView


class mainwindow(QMainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.ui = uic.loadUi('form.ui', self)
        logging.basicConfig(level=logging.DEBUG)
        # file = QFile(":/dark/stylesheet.qss")
        # file.open(QIODevice.OpenModeFlag.ReadOnly)
        # stream = QTextStream(file)
        # self.setStyleSheet(stream.readAll())
        # selected = QInputDialog.getItem(self, self.tr("Choose dataset type"), self.tr("Choose dataset type"), DatasetType.keys())
        # print(selected)
        dataset_path = "/home/biblbrox/Projects/Prometei/nn/dataset/video_from_prometei/normal/"
        dataset = Dataset(DatasetType.KITTI_IMG, '/home/biblbrox/autonet/test_kitti/')
        images, labels = dataset.get_labeled()
        classes = dataset.classes_dict
        diagram = ui.make_diagram(self, classes)
        dataset_info = PyQt6.QtWidgets.QLabel(self)
        dataset_info.setText(f"Images count: {len(images)}, Labeled: {len(labels)}")

        data = {'Images count': [],
                'Label count': [],
                'Labeled': []}

        for type, count in classes.items():
            data['Images count'].append(count)


        table = TableView(data, 3, 4)

        self.gridLayout.addWidget(diagram, 0, 0)
        self.gridLayout.addWidget(dataset_info, 0, 1)
        self.gridLayout.addWidget(table, 1, 0)
        #self.gridLayout.addWidget(fig3, 1, 0)
        #self.gridLayout.addWidget(fig4, 1, 1)
        #self.setCentralWidget(fig)


if __name__ == "__main__":
    app = QApplication([])
    widget = mainwindow()
    widget.show()
    sys.exit(app.exec())
