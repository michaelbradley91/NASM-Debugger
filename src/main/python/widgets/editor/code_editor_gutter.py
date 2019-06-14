from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QWidget


class CodeEditorGutter(QWidget):
    """ The gutter of the code editor window. """
    def __init__(self, editor):
        self.editor = editor
        super().__init__(editor)

    def sizeHint(self) -> QSize:
        return QSize(self.editor.gutter_area_width, 0)

    def paintEvent(self, event: QPaintEvent):
        self.editor.gutter_paint_event(event)
