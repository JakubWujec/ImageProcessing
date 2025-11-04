from abc import abstractmethod
from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import (
    QPainter,
)


class DrawingTool:
    @abstractmethod
    def draw(self, painter: QPainter, start_point: QPoint, end_point: QPoint):
        raise NotImplementedError()


class CircleTool(DrawingTool):
    def draw(self, painter: QPainter, start_point: QPoint, end_point: QPoint):
        radius = (start_point - end_point).manhattanLength()
        painter.drawEllipse(start_point, radius, radius)


class RectangleTool(DrawingTool):
    def draw(self, painter: QPainter, start_point: QPoint, end_point: QPoint):
        rect = QRect(start_point, end_point)
        painter.drawRect(rect.normalized())


class LineTool(DrawingTool):
    def draw(self, painter: QPainter, start_point: QPoint, end_point: QPoint):
        painter.drawLine(start_point, end_point)


class PenTool(DrawingTool):
    def draw(self, painter: QPainter, start_point: QPoint, end_point: QPoint):
        painter.drawLine(start_point, end_point)


class TextTool(DrawingTool):
    def __init__(self) -> None:
        self.textToDraw = ""
        super().__init__()

    def draw(self, painter: QPainter, start_point: QPoint, end_point: QPoint):
        painter.drawText(start_point, self.textToDraw)
