import os.path
import sys
import traceback
from types import TracebackType

import matplotlib
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox

from dataset.dataset import DatasetType, DatasetItem
from translate import tr

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.subplots()
        super(MplCanvas, self).__init__(fig)


def make_diagram(parent, values: dict):
    sc = MplCanvas(parent)
    labels = values.keys()
    sizes = [count / len(values) for label, count in values.items()]
    sc.axes.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)

    return sc


def show_failure_message(message: str, tback: TracebackType = None):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(tr("Error message: "))
    msg.setInformativeText(message)
    msg.setWindowTitle(tr("Failure message"))
    msg.setDetailedText(str(traceback.format_tb(tback)))
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    return msg.exec_()


class Formatter:
    def __init__(self, dataset_item: DatasetItem):
        self.dataset_item = dataset_item


class KittiImgFormatter(Formatter):
    def __format__(self, format_spec):
        return format(str(self), format_spec)
