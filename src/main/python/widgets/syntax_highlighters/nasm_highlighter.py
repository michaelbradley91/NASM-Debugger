from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QSyntaxHighlighter, QTextDocument


class NASMHighlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument):
        super().__init__(document)

        highlighting_rules = []

        keywords = "eax", "ebx"
        for keyword in keywords:
            rule = HighlightingRule()
            rule.pattern = QRegularExpression(keyword);
            rule.format = keywordFormat;
            highlightingRules.append(rule);

    def highlightBlock(self, text: str):
        QRegularExpressionMatchIterator matchIterator = rule.pattern.globalMatch(text);
            while (matchIterator.hasNext()) {
                QRegularExpressionMatch match = matchIterator.next();
                setFormat(match.capturedStart(), match.capturedLength(), rule.format);
            }