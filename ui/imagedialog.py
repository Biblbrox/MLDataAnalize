import PyQt5
from PyQt5.QtGui import QPixmap, QImage


class ImageDialog(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.image_lbl = PyQt5.QtWidgets.QLabel()
        lay = PyQt5.QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.image_lbl)

    def set_image(self, image: QImage):
        pixmap = QPixmap.fromImage(image)
        self.image_lbl.setPixmap(QPixmap(pixmap))