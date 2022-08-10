import os.path

from PyQt6.QtWidgets import QGridLayout, QWidget

from ui.imagelabel import ImageLabel


class ImageGallery(QGridLayout):
    def __init__(self, images_files, image_classes, parent=None):
        QWidget.__init__(self, parent)
        for image_file in images_files:
            assert (os.path.exists(image_file))
        assert(len(image_classes) == len(images_files))

        self.images_files = images_files

        cols = 4
        i = 0
        while True:
            for j in range(cols):
                if i + j >= len(images_files):
                    return

                img = ImageLabel(images_files[i + j], image_classes[i + j])
                self.addWidget(img, i, j)

            i += 1
