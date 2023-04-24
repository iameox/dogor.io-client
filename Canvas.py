from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QLabel


class Canvas(QLabel):
    def __init__(self):
        super().__init__()

        self.__goals = list()
        self.__entities = list()

    def goals(self, goals) -> None:
        self.__goals = goals

    def entities(self, entities) -> None:
        self.__entities = entities

    def setup(self) -> None:
        self.setStyleSheet('background-color: black;')

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.scale(0.1, 0.1)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(Qt.GlobalColor.gray))

        for goal in self.__goals:
            point = QPoint(goal['position']['x'], goal['position']['y'])
            painter.drawEllipse(point, goal['radius'], goal['radius'])

        for entity in self.__entities:
            match entity['type']:
                case 0:
                    painter.setBrush(QBrush(QColor(230, 240, 240)))
                case 1:
                    painter.setBrush(QBrush(Qt.GlobalColor.blue))
                case 2:
                    painter.setBrush(QBrush(Qt.GlobalColor.cyan))
                case 3:
                    painter.setBrush(QBrush(Qt.GlobalColor.green))
                case 4:
                    painter.setBrush(QBrush(Qt.GlobalColor.magenta))
                case 5:
                    painter.setBrush(QBrush(Qt.GlobalColor.red))
                case 6:
                    painter.setBrush(QBrush(Qt.GlobalColor.yellow))

            point = QPoint(entity['position']['x'], entity['position']['y'])
            painter.drawEllipse(point, entity['radius'], entity['radius'])
