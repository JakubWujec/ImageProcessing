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


class Canvas(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.image = QImage(self.size(), QImage.Format.Format_RGBA8888)
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.drawing = False

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

        if self.drawing:
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)

            self.drawCircle(painter, self.startPoint, self.endPoint)

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if a0:
            if a0.button() == Qt.MouseButton.LeftButton:
                self.startPoint = a0.position().toPoint()
                self.endPoint = a0.position().toPoint()
                self.drawing = True
            if a0.button() == Qt.MouseButton.RightButton:
                self.getImagePainter().drawImage(0, 0, self.image)
                # self.clear(self.image)
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if a0 and self.drawing:
            self.endPoint = a0.position().toPoint()
            self.update()

        return super().mouseMoveEvent(a0)

    def getImagePainter(self):
        return QPainter(self.image)

    def mouseReleaseEvent(self, a0: QMouseEvent | None):
        if a0 and a0.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.endPoint = a0.position().toPoint()
            self.drawing = False
            self.drawCircle(self.getImagePainter(), self.startPoint, self.endPoint)

    def drawLine(self, painter: QPainter, startPoint: QPoint, endPoint: QPoint):
        painter.drawLine(startPoint, endPoint)

    def drawCircle(self, painter: QPainter, start_point: QPoint, end_point: QPoint):
        radius = (start_point - end_point).manhattanLength()
        painter.drawEllipse(start_point, radius, radius)

    def drawRectangle(self, painter: QPainter, start_point: QPoint, end_point: QPoint):
        rect = QRect(start_point, end_point)
        painter.drawRect(rect.normalized())

    def clear(self, image):
        image.fill(Qt.GlobalColor.transparent)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.image = QImage(self.size(), QImage.Format.Format_RGBA8888)
        self.image.fill(Qt.GlobalColor.transparent)
        super().resizeEvent(a0)
