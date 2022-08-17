from abc import ABC, abstractmethod
from enum import Enum
import os

import torch.utils.data
import torchvision.datasets
import logging
import numpy as np
from collections import Counter
import cv2 as cv
from torch.utils.data.dataset import T_co

from torchvision.transforms import transforms

DatasetTypesNames = {'Kitti Images only': 'Kitti Images only', 'YOLO': 'YOLO', 'Kitti': 'Kitti'}


class DatasetType(Enum):
    YOLO = 0
    KITTI_IMG = 1
    KITTI = 2


class DatasetValidator(ABC):
    @abstractmethod
    def validate(self) -> bool:
        ...


class KittiValidator(DatasetValidator):
    def validate(self) -> bool:
        return True


class KittiImgValidator(DatasetValidator):
    def validate(self) -> bool:
        return True


class YoloValidator(DatasetValidator):
    def validate(self) -> bool:
        return True


class Bbox2D:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


class Formatter(ABC):
    @abstractmethod
    def generate_label_obj(self, label_file: str) -> np.array:
        ...

    @abstractmethod
    def generate_target_obj(self, target_file: str):
        ...

    @abstractmethod
    def generate_bboxes(self, label_file: str) -> np.array([Bbox2D]):
        ...


"""
Kitti format description
Values    Name      Description
----------------------------------------------------------------------------
   1    type         Describes the type of object: 'Car', 'Van', 'Truck',
                     'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
                     'Misc' or 'DontCare'
   1    truncated    Float from 0 (non-truncated) to 1 (truncated), where
                     truncated refers to the object leaving image boundaries
   1    occluded     Integer (0,1,2,3) indicating occlusion state:
                     0 = fully visible, 1 = partly occluded
                     2 = largely occluded, 3 = unknown
   1    alpha        Observation angle of object, ranging [-pi..pi]
   4    bbox         2D bounding box of object in the image (0-based index):
                     contains left, top, right, bottom pixel coordinates
   3    dimensions   3D object dimensions: height, width, length (in meters)
   3    location     3D object location x,y,z in camera coordinates (in meters)
   1    rotation_y   Rotation ry around Y-axis in camera coordinates [-pi..pi]
   1    score        Only for results: Float, indicating confidence in
                     detection, needed for p/r curves, higher is better.
"""


class KittyFormatter(Formatter):
    def generate_label_obj(self, label_file: str) -> np.array:
        assert (os.path.exists(label_file))

        label_data = np.array([])
        with open(label_file, 'r') as f:
            for line in f.readlines():
                row_dict = {}
                line = line.split()
                row_dict['type'] = line[0]
                row_dict['truncated'] = float(line[1])
                row_dict['occluded'] = float(line[2])
                row_dict['alpha'] = float(line[3])
                row_dict['bbox'] = np.array([line[4], line[5], line[6], line[7]]).astype(np.float)
                row_dict['dimensions'] = np.array([line[8], line[9], line[10]]).astype(np.float)
                row_dict['location'] = np.array([line[11], line[12], line[13]]).astype(np.float)
                row_dict['rotation_y'] = float(line[14])
                label_data = np.append(label_data, row_dict)

        return label_data

    def generate_bboxes(self, label_file: str) -> np.array([Bbox2D]):
        objects = self.generate_label_obj(label_file)
        bboxes = np.array([])
        for obj in objects:
            x, y = obj['bbox'][0], obj['bbox'][1]
            width, height = obj['dimensions'][0], obj['dimensions'][1]
            bbox = Bbox2D(x, y, x + width, y + width)
            bboxes = np.append(bboxes, [bbox])

        return bboxes

    def generate_target_obj(self, target_file: str):
        assert (os.path.exists(target_file))

        target_obj = cv.imread(target_file)
        if not target_obj:
            raise ValueError(f"Unable to open target file {target_file}")

        return target_obj


"""
YOLO format description
Values    Name      Description
----------------------------------------------------------------------------
   1    type          Integer number of object from 0 to (classes-1). 
                      Describes the type of object: 'Car', 'Van', 'Truck',
                     'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
                     'Misc' or 'DontCare'
   1    x            <x> = <absolute_x> / <image_width>.  Float value relative to width of image,
                     it can be equal from (0.0 to 1.0]. Describes center of rectangle
   1    y            <y> = <absolute_y> / <image_width>.  Float value relative to height of image, 
                     it can be equal from (0.0 to 1.0]. Describes center of rectangle
   1    width        <width> = <absolute_width> / <image_width>. Object width relative to image width. 
   1    height       <height> = <absolute_height> / <image_height>. Object width relative to image width.
"""


class YOLOFormatter(Formatter):
    def generate_label_obj(self, label_file: str) -> np.array:
        assert (os.path.exists(label_file))

        label_data = np.array([])
        with open(label_file, 'r') as f:
            for line in f.readlines():
                row_dict = {}
                line = line.split()
                row_dict['type'] = line[0]
                row_dict['x'] = float(line[1])
                row_dict['y'] = float(line[2])
                row_dict['width'] = float(line[3])
                row_dict['height'] = float(line[4])
                label_data = np.append(label_data, row_dict)

        return label_data

    def generate_bboxes(self, label_file: str) -> np.array([Bbox2D]):
        objects = self.generate_label_obj(label_file)
        bboxes = np.array([])
        for obj in objects:
            bbox = Bbox2D(obj['x'], obj['y'], obj['x'] + obj['width'], obj['y'] + obj['height'])
            bboxes = np.append(bboxes, [bbox])

        return bboxes

    def generate_target_obj(self, target_file: str):
        assert (os.path.exists(target_file))

        target_obj = cv.imread(target_file)
        if not target_obj:
            raise ValueError(f"Unable to open target file {target_file}")

        return target_obj


class FormatterFactory:
    def __init__(self):
        self._creators = {}

    def register_format(self, fmt, creator):
        assert (callable(creator))
        self._creators[fmt] = creator

    def get_formatter(self, fmt: DatasetType):
        creator = self._creators.get(fmt)
        if not creator:
            raise ValueError(f"Dataset formatter for format {fmt} is not registered")
        return creator()


class DatasetFactory:
    def __init__(self):
        self._creators = {}

    def register_format(self, fmt, creator):
        assert (callable(creator))
        self._creators[fmt] = creator

    def get_formatter(self, fmt: DatasetType):
        creator = self._creators.get(fmt)
        if not creator:
            raise ValueError(f"Dataset with format {fmt} is not registered")
        return creator()


class DatasetItem:
    """
    Contain info about single dataset object. For example for label and image
    Obj file may image, point cloud, etc. Label usually text file
    """

    def __init__(self, formatter: Formatter, target_file, label_file):
        self.type = type
        self.label_file = target_file
        self.target_file = label_file
        self.formatter = formatter

    def get_obj(self):
        return self.formatter.generate_target_obj(self.target_file)

    def get_label_data(self):
        return self.formatter.generate_label_obj(self.label_file)

    def get_bboxes(self):
        return self.formatter.generate_bboxes(self.label_file)


class YOLODataset(torch.utils.data.Dataset):

    def __getitem__(self, index) -> T_co:
        pass


KittiDataset = torchvision.datasets.Kitti


class Dataset:
    def __init__(self, type: DatasetType, root_folder: str):
        if not os.path.exists(root_folder):
            raise RuntimeError(f"Folder {root_folder} doesn't exists")

        self.type = type
        self.root_folder = root_folder
        self.items = np.array([])

        if self.type == DatasetType.YOLO:
            logging.debug("YOLO dataset selected")
        elif self.type == DatasetType.KITTI or self.type == DatasetType.KITTI_IMG:
            logging.debug("KITTI dataset selected")
            self.train = KittiDataset(root_folder, train=True, download=False,
                                      transform=transforms.ToTensor())
            self.test = KittiDataset(root_folder, train=False, download=False,
                                     transform=transforms.ToTensor())

            # Filter not existing labels. Image exsits but not label
            self.train.targets = [target_file for target_file in self.train.targets if os.path.exists(target_file)]

            for obj_file, label_file in zip(self.train.targets, self.train.images):
                self.items = np.append(self.items, [DatasetItem(KittyFormatter(), obj_file, label_file)])

            classes = np.array([])
            for item in self.items:
                for obj in item.get_label_data():
                    classes = np.append(classes, obj['type'])

            self.classes_dict = Counter(classes)

    def get_objects_gen(self):
        def generator():
            for item in self.items:
                item_data = item.get_label_data()
                yield item_data

        return generator()

    '''
    Return labeled items. For example [img, label_file].
    Specific format may depend from the dataset type.
    '''

    def get_labeled(self):
        if self.type == DatasetType.KITTI_IMG:
            images = self.train.images
            labels = self.train.targets

            return images, labels
