from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QTextCharFormat
from dataclasses import dataclass


@dataclass
class HighlightingRule:
    pattern: QRegularExpression
    format: QTextCharFormat
