import logging
import os.path

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGridLayout, QWidget

from ui.imagedialog import ImageDialog
from ui.imagelabel import ImageLabel


class ImageGallery(QGridLayout):

    tip_signal = PyQt5.QtCore.pyqtSignal(PyQt5.QtCore.QPoint, str)

    def on_open_action(self, image_path):
        logging.debug("On open action")
        dialog = ImageDialog(self.parent)
        dialog.set_image(QImage(image_path))
        dialog.show()

    def on_label_action(self, image_path):
        logging.debug("On label action")

    def on_tip_action(self, pos: PyQt5.QtCore.QPoint, image_path):
        self.tip_signal.emit(pos, image_path)
        logging.debug("On tip action")

    def __init__(self, images_files, el_classes, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent

        for image_file in images_files:
            assert (os.path.exists(image_file))
        assert (len(el_classes) == len(images_files))

        self.images_files = images_files

        cols = 4
        row = 0
        el_cnt = 0
        while True:
            for col in range(cols):
                if el_cnt >= len(images_files):
                    return

                img = ImageLabel(images_files[el_cnt], el_classes[el_cnt], self.parent)

                img.open_signal.connect(self.on_open_action)
                img.label_signal.connect(self.on_label_action)
                img.tip_signal.connect(self.on_tip_action)

                self.addWidget(img, row, col)
                el_cnt += 1

            row += 1
