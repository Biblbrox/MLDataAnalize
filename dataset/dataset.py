from enum import Enum
import os
import torchvision.datasets
import logging
import numpy as np
from collections import Counter
import cv2 as cv

from torchvision.transforms import transforms


class DatasetType(Enum):
    YOLO = 0
    KITTI_IMG = 1
    KITTI = 2


class KittyFormater:
    def __init__(self):
        pass

    def generate_dict(self, label_file):



class DatasetItem:
    """
    Contain info about single dataset object. For example for label and image
    Obj file may image, point cloud, etc. Label usually text file
    """

    def __init__(self, type: DatasetType, obj_file, label_file):
        self.type = type
        self.label_file = obj_file
        self.target_file = label_file

    def get_obj(self):
        if self.type == DatasetType.KITTI_IMG:
            return cv.imread(self.target_file)

    def get_label(self):
        if self.type == DatasetType.KITTI_IMG:
            label_data = np.array([])
            with open(self.label_file, 'r') as f:
                for line in f.readlines():
                    label_data = np.append(label_data, [line.split(' ')])
            print(f"Label data: {label_data}")


class Dataset:
    def __init__(self, type: DatasetType, root_folder: str):
        if not os.path.exists(root_folder):
            raise RuntimeError(f"Folder {root_folder} doesn't exists")

        self.type = type
        self.items = np.array([])

        if self.type == DatasetType.YOLO:
            logging.debug("YOLO dataset selected")
        elif self.type == DatasetType.KITTI:
            logging.debug("KITTI dataset selected")
        elif self.type == DatasetType.KITTI_IMG:
            logging.debug("KITTI_IMG dataset selected")
            self.train = torchvision.datasets.Kitti(root_folder, train=True, download=False,
                                                    transform=transforms.ToTensor())
            self.test = torchvision.datasets.Kitti(root_folder, train=False, download=False,
                                                   transform=transforms.ToTensor())

            for obj_file, label_file in zip(self.train.targets, self.train.images):
                self.items = np.append(self.items, [DatasetItem(self.type, obj_file, label_file)])

            # Filter not existing labels. Image exsits but not label
            self.train.targets = [target_file for target_file in self.train.targets if os.path.exists(target_file)]

            # Find all possible classes in dataset
            label_files = self.train.targets
            print(f"Label files: {label_files}")
            classes = np.array([])
            for label_file in label_files:
                with open(label_file, 'r') as f:
                    for line in f.readlines():
                        classes = np.append(classes, line.split()[0])

            for item in self.items:
                item.get_label()

            self.classes_dict = Counter(classes)

    '''
    Return labeled items. For example [img, label_file].
    Specific format may depend from the dataset type.
    '''

    def get_labeled(self):
        if self.type == DatasetType.KITTI_IMG:
            images = self.train.images
            labels = self.train.targets

            return images, labels
