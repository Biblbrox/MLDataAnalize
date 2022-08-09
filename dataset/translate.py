from PyQt6 import QtCore


def tr(message: str):
    return QtCore.QObject.tr(message)
