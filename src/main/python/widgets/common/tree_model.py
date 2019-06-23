from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt


class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def append_child(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def child_count(self):
        return len(self.childItems)

    def column_count(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(("Title", "Summary"))
        self.setupModelData(data.split('\n'), self.rootItem)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self.rootItem.column_count()

    def data(self, index: QModelIndex, role: int = ...) -> any:
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()

        if parent_item == self.rootItem:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()
