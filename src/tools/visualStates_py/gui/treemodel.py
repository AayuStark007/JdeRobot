'''
   Copyright (C) 1997-2016 JDERobot Developers Team
 
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
 
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Library General Public License for more details.
 
   You should have received a copy of the GNU General Public License
   along with this program; if not, see <http://www.gnu.org/licenses/>.
 
   Authors : Samuel Rey <samuel.rey.escudero@gmail.com> 
 
  '''

from PyQt5.QtCore import Qt, QModelIndex, QAbstractItemModel
from .treenode import TreeNode

class TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rootNode = TreeNode("ID", "Name", "white")

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootNode.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            item = index.internalPointer()
            return item.data(index.column())

        elif role == Qt.BackgroundColorRole:
            item = index.internalPointer()
            return item.background()

        return None

    def rowId(self, index):
        if not index.isValid():
            return 0

        if not index.parent().isValid():
            item = index.internalPointer()
            return item.id
        else:
            return 0

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootNode.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootNode
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def indexOf(self, child):
        return self.createIndex(child.row(), 0, child)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootNode:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootNode
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def insertState(self, state, color, parent=None):
        if parent is None:
            parent = self.rootNode
        newNode = TreeNode(state.stateData.id, state.stateData.name, color, parent)
        parent.appendChild(newNode)
        # TODO: this redraws whole tree, just update according to the insertion
        self.layoutChanged.emit()

    def removeState(self, state, parent=None):
        if parent is None:
            parent = self.rootNode
        childToBeRemoved = None
        for s in parent.getChildren():
            if s.id == state.id:
                childToBeRemoved = s
                break

        if childToBeRemoved != None:
            print('remove child.id:' + str(childToBeRemoved.id))
            parent.removeChild(childToBeRemoved)
            self.layoutChanged.emit()

    def getChildren(self):
        return self.rootNode.childItems

    def getByDataId(self, id):
        for item in self.getChildren():
            if item.id == id:
                return item
        return None

    def removeAll(self):
        self.rootNode.removeChildren()
        self.layoutChanged.emit()
