from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self):
        hor_headers = []
        for n, key in enumerate(sorted(self.data.keys())):
            hor_headers.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(hor_headers)
