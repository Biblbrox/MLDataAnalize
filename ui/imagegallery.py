import os.path

from PyQt6.QtWidgets import QGridLayout, QWidget

from ui.imagelabel import ImageLabel


class ImageGallery(QGridLayout):
    def __init__(self, images_files, parent=None):
        QWidget.__init__(self, parent)
        for image_file in images_files:
            assert (os.path.exists(image_file))

        self.images_files = images_files

        rows = 10
        cols = 4
        k = 0
        indices = []
        # Find indices
        stop = False
        for i in range(rows):
            if stop:
                break
            for j in range(cols):
                if k >= len(images_files):
                    stop = True
                    break

                indices.append([i, j])
                k += 1

        for i, j in indices:
            label_img = ImageLabel(images_files[i + j])
            self.addWidget(label_img, i, j)



