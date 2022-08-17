from typing import List

import numpy as np
import imgaug.augmenters as iaa
from imgaug import ia

from dataset.dataset import Dataset, DatasetItem

"""
Augment images with specific augmentation sequential 
"""
def augment(items: List[DatasetItem], seq: iaa.Sequential) -> List[DatasetItem]:
    ia.seed(1)

    labels_res = []
    images_res = []
    for item in items:
        image = item.get_obj()
        bboxes = item.get_bboxes()
        # Augment BBs and images.
        image_aug, bbs_aug = seq(image=image, bounding_boxes=bboxes)

        # for i in range(len(label.getBoundingBoxes())):
        #    before = label.getBoundingBoxes()[i]
        #    after = bbs_aug.bounding_boxes[i]
        #    print("BB %d: (%.4f, %.4f, %.4f, %.4f) -> (%.4f, %.4f, %.4f, %.4f)" % (
        #        i,
        #        before.x1, before.y1, before.x2, before.y2,
        #        after.x1, after.y1, after.x2, after.y2)
        #          )

        label_aug = labelFromBoxes(label.shape, label.obj_type, bbs_aug)
        labels_res.append(label_aug)
        images_res.append(image_aug)


    return images_res, labels_res



class Augmentation:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def rotate(self):


    def crop(self):
