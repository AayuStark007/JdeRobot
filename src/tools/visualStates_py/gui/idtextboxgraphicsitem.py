from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtCore import Qt, pyqtSignal

class IdTextBoxGraphicsItem(QGraphicsTextItem):

    textChanged = pyqtSignal('QString')
    textEditStarted = pyqtSignal()
    textEditFinished = pyqtSignal()

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.name = name


    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == Qt.NoTextInteraction:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
            self.textEditStarted.emit()

        super().mouseDoubleClickEvent(event)


    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.textChanged.emit(self.toPlainText())
        self.textEditFinished.emit()
        super().focusOutEvent(event)
