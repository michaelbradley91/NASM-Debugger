from typing import List


class AppearanceTreeItem:
    def __init__(self, data: List[any], parent: "AppearanceTreeItem" = None):
        self.data = data
        self.parent = parent

    def append_child(self):
public:
    explicit TreeItem(const QVector<QVariant> &data, TreeItem *parentItem = nullptr);
    ~TreeItem();

    void appendChild(TreeItem *child);

    TreeItem *child(int row);
    int childCount() const;
    int columnCount() const;
    QVariant data(int column) const;
    int row() const;
    TreeItem *parentItem();

private:
    QVector<TreeItem*> m_childItems;
    QVector<QVariant> m_itemData;
    TreeItem *m_parentItem;
};