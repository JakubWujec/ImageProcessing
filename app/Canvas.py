from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
)
from PyQt6.QtGui import (
    QImage,
    QPainter,
    QPaintEvent,
    QMouseEvent,
    QResizeEvent,
    QPen,
    QColor,
)

from app.DrawingTool import DrawingTool, LineTool, PenTool, RectangleTool


class Canvas(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.image = QImage(self.size(), QImage.Format.Format_RGBA8888)
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.previousPoint = QPoint()
        self.drawing = False
        self.currentTool: DrawingTool = RectangleTool()
        self.setMouseTracking(True)

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

        if self.drawing:
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)

            if not isinstance(self.currentTool, PenTool):
                self.currentTool.draw(painter, self.startPoint, self.endPoint)

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if a0:
            if a0.button() == Qt.MouseButton.LeftButton:
                self.startPoint = a0.position().toPoint()
                self.endPoint = a0.position().toPoint()
                self.drawing = True
                self.previousPoint = self.startPoint
            if a0.button() == Qt.MouseButton.RightButton:
                self.clear(self.image)
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if a0 and self.drawing:
            self.endPoint = a0.position().toPoint()
            self.update()

            if isinstance(self.currentTool, PenTool):
                self.currentTool.draw(
                    self.getImagePainter(), self.previousPoint, self.endPoint
                )

            self.previousPoint = self.endPoint

        return super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QMouseEvent | None):
        if a0 and a0.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.endPoint = a0.position().toPoint()
            self.drawing = False

            if not isinstance(self.currentTool, PenTool):
                self.drawWithCurrentTool()

    def getImagePainter(self):
        return QPainter(self.image)

    def drawWithCurrentTool(self):
        self.currentTool.draw(self.getImagePainter(), self.startPoint, self.endPoint)

    def clear(self, image):
        image.fill(Qt.GlobalColor.transparent)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.image = QImage(self.size(), QImage.Format.Format_RGBA8888)
        self.image.fill(Qt.GlobalColor.transparent)
        super().resizeEvent(a0)
