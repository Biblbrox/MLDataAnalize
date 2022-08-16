# This Python file uses the following encoding: utf-8
import os.path
import sys

import importlib

import PyQt5.QtWidgets
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QWidget, QMessageBox
from PyQt5 import uic, QtCore

from dataset.dataset import DatasetType, Dataset, DatasetTypesNames
from translate import tr
from ui import ui

import logging

from dataset.table import TableView
from ui.imagegallery import ImageGallery


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('form.ui', self)
        logging.basicConfig(level=logging.DEBUG)

        self.dataset_selection_combo = PyQt5.QtWidgets.QComboBox(self)

        self.dataset_type = DatasetType.KITTI_IMG
        logging.debug(f"Current dataset type: {self.dataset_type}")

        self.dataset = None

        self.init_toolbar()
        self.actionOpen_dataset.triggered.connect(self.on_action_open_dataset)
        self.dataset_selection_combo.currentTextChanged.connect(self.on_dataset_type_changed)

        self.init_dataset_overview()
        self.init_diagram_cell()
        self.init_info_cell()
        # self.init_table_cell()

    def on_dataset_type_changed(self, type_name):
        assert (type_name in DatasetTypesNames.keys())
        self.dataset_type = DatasetTypesNames[type_name]
        logging.debug(f"Dataset type changed to: {type_name}")

    def on_action_open_dataset(self):
        dataset_path = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self, tr("Select dataset root folder"))
        if self.dataset_type == DatasetType.KITTI_IMG:
            self.dataset = Dataset(DatasetType.KITTI_IMG, dataset_path)
            self.images, self.labels = self.dataset.get_labeled()
            self.image_classes = []
            for i in range(len(self.images)):
                self.image_classes.append('ImageLabelLabeled' if i < len(self.labels) else 'ImageLabelUnlabeled')
            self.update_info()
        # dataset_type =

    def update_info(self):
        logging.debug("Updating dataset info")
        if self.dataset is None:
            return

        self.init_info_cell()
        self.init_dataset_overview()
        self.init_diagram_cell()

    def init_diagram_cell(self):
        if self.dataset is None:
            return

        classes = self.dataset.classes_dict
        diagram = ui.make_diagram(self, classes)
        diagram.set_window_title(tr("Classes distribution"))
        self.gridLayout.addWidget(diagram, 0, 0)

    def init_info_cell(self):
        if self.dataset is None:
            return

        dataset_info = PyQt5.QtWidgets.QLabel(self)
        images_info = f"Images count: {len(self.images)}"
        labels_info = f"Labels count: {len(self.labels)}"
        obj_count = sum(len(obj) for obj in self.dataset.get_objects_gen())
        objects_info = f"Total number of objects (instances): {obj_count}"
        dataset_info.setText(f"{images_info}\n{labels_info}\n{objects_info}")
        dataset_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft and QtCore.Qt.AlignmentFlag.AlignTop)
        self.gridLayout.addWidget(dataset_info, 0, 1)

    def init_table_cell(self):
        if self.dataset is None:
            return

        classes = self.dataset.classes_dict
        data = {'Classes': classes.keys(),
                'Images': [1, 2]
                }

        table = TableView(data, 3, 4)
        self.gridLayout.addWidget(table, 1, 0)

    def init_dataset_overview(self):
        if self.dataset is None:
            return

        image_gallery = ImageGallery(self.images, self.image_classes, self)
        image_gallery.tip_signal.connect(self.on_dataset_overview_tip)
        self.scrollAreaWidgetContents.setLayout(image_gallery)

    def on_dataset_overview_tip(self, pos, image_file):
        if image_file not in self.images:
            return

        label_file = dict(zip(self.images, self.labels))[image_file]
        with open(label_file) as f:
            label_info = f.readlines()

        font = QFont()
        font.setFamily("Serif")
        QToolTip.setFont(font)
        QToolTip.showText(pos, "".join(label_info))

    def init_toolbar(self):
        dataset_type_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self.dataset_selection_combo.setObjectName("dataset_selection_combo")
        self.dataset_selection_combo.addItems(DatasetTypesNames)
        self.dataset_selection_combo.setItemData(0, DatasetTypesNames)
        self.dataset_selection_combo.setPlaceholderText(tr("Select dataset type:"))
        dataset_selection_label = PyQt5.QtWidgets.QLabel(tr("Select dataset type:"))
        dataset_type_layout.addWidget(dataset_selection_label)
        dataset_type_layout.addWidget(self.dataset_selection_combo)
        placeholder_widget = QWidget(self)
        placeholder_widget.setLayout(dataset_type_layout)
        self.toolBar.addWidget(placeholder_widget)


class Application(QApplication):
    def notify(self, obj: QObject, event: QEvent):
        exc_occurred = False
        try:
            return QApplication.notify(self, obj, event)
        except Exception as err:
            exc_occurred = True
            return False
        finally:
            if exc_occurred:
                self.quit()


def my_excepthook(type, err_msg: str, tback):
    # log the exception here
    logging.error(f"Unhandled exception occurred: {err_msg}")
    ui.show_failure_message(None, f"Unhandled exception: {err_msg}", tback)
    # then call the default handler
    sys.__excepthook__(type, err_msg, tback)


sys.excepthook = my_excepthook

if __name__ == "__main__":
    logging.basicConfig(
        # filename='HISTORYlistener.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    app = Application([])
    with open("./styles/styles.qss") as styles:
        app.setStyleSheet("".join(styles.readlines()))
    widget = MainWindow()
    widget.show()
    app.exec()
    sys.exit()
