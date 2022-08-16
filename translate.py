from PyQt5 import QtCore
from PyQt5.QtCore import QObject


def tr(message: str):
    obj = QObject()
    return QtCore.QObject.tr(obj, message)
