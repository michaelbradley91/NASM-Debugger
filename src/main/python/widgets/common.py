from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget


class ThinFrame(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self.setMidLineWidth(0)
        self.setLineWidth(0)
        self.setContentsMargins(0, 0, 0, 0)


class ThinVBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class ThinHBoxLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
