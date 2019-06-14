from PyQt5.QtCore import pyqtSlot, QRect, Qt
from PyQt5.QtGui import QPaintEvent, QResizeEvent, QColor, QTextFormat, QPainter
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QTextEdit

from widgets.editor.code_editor_gutter import CodeEditorGutter


class CodeEditor(QPlainTextEdit):
    # noinspection PyUnresolvedReferences
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.gutter = CodeEditorGutter(self)
        # Block count changed corresponds to a new line
        self.blockCountChanged.connect(self.update_gutter_area_width)
        self.updateRequest.connect(self.update_gutter)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_gutter_area_width(number_of_lines=0)
        self.highlight_current_line()

    def gutter_paint_event(self, event: QPaintEvent):
        painter = QPainter(self.gutter)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                line_number = block_number + 1
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.gutter.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, str(line_number))

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    @property
    def gutter_area_width(self):
        # Get the number of digits required for the line numbers
        digits = 1
        number_of_lines = max(1, self.blockCount())
        while number_of_lines >= 10:
            number_of_lines /= 10
            digits += 1

        # Compute the width based on the font
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    # noinspection PyUnusedLocal
    @pyqtSlot(int)
    def update_gutter_area_width(self, number_of_lines: int):
        self.setViewportMargins(self.gutter_area_width, 0, 0, 0)

    @pyqtSlot()
    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor(Qt.yellow).lighter(160))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            # State that the highlighting should be where the cursor is
            selection.cursor = self.textCursor()

            # Clear the selection made by the user for this calculation. This means the selection fills
            # the whole line because of the full width selection. Visually, the cursor is now just on the line.
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    @pyqtSlot(QRect, int)
    def update_gutter(self, rect: QRect, vertical_scroll_pixels: int):
        if vertical_scroll_pixels:
            self.gutter.scroll(0, vertical_scroll_pixels)

        self.gutter.update(0, rect.y(), self.gutter.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_gutter_area_width(0)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        rect = self.contentsRect()
        self.gutter.setGeometry(rect.x(), rect.y(), self.gutter_area_width, rect.height())
