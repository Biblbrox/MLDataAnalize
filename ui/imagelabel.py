import logging
import os.path

import PyQt5.QtWidgets
import PyQt5.QtCore
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap, QHelpEvent


class ImageLabel(PyQt5.QtWidgets.QLabel):
    open_signal = PyQt5.QtCore.pyqtSignal(str)
    label_signal = PyQt5.QtCore.pyqtSignal(str)
    tip_signal = PyQt5.QtCore.pyqtSignal(PyQt5.QtCore.QPoint, str)

    def __init__(self, image_path, object_name, parent=None):
        PyQt5.QtWidgets.QWidget.__init__(self, parent)
        assert (os.path.exists(image_path))

        self.image_path = image_path
        orig = QImage(self.image_path)
        scaled = orig.scaled(120, 120)
        self.setObjectName(object_name)
        self.setPixmap(QPixmap().fromImage(scaled))

        outer_vertical_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        outer_vertical_layout.addWidget(PyQt5.QtWidgets.QLabel(os.path.basename(self.image_path)))

        buttons_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        hor_layout = PyQt5.QtWidgets.QHBoxLayout(self)
        hor_layout.addSpacing(100)
        vert_laoyut = PyQt5.QtWidgets.QVBoxLayout()
        self.open_button = PyQt5.QtWidgets.QPushButton("Open")
        self.label_button = PyQt5.QtWidgets.QPushButton("Label")
        self.open_button.setFixedSize(40, 40)
        self.label_button.setFixedSize(40, 40)

        vert_laoyut.addWidget(self.open_button)
        vert_laoyut.addWidget(self.label_button)
        hor_layout.addLayout(vert_laoyut)
        buttons_layout.addLayout(hor_layout)
        outer_vertical_layout.addLayout(buttons_layout)
        self.setLayout(outer_vertical_layout)

        self.open_button.clicked.connect(self.onOpenButtonClicked)
        self.label_button.clicked.connect(self.onLabelButtonClicked)

    def event(self, e: QtCore.QEvent) -> bool:
        if e.type() == QtCore.QEvent.Type.ToolTip:
            self.tip_signal.emit(e.globalPos(), self.image_path)

            return True

        return super(ImageLabel, self).event(e)

    def onOpenButtonClicked(self):
        self.open_signal.emit(self.image_path)

    def onLabelButtonClicked(self):
        self.label_signal.emit(self.image_path)
