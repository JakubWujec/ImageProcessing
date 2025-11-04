from PyQt6.QtCore import Qt, QPoint, QRect

from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
)
from PyQt6.QtGui import (
    QImage,
    QKeyEvent,
    QPainter,
    QPaintEvent,
    QMouseEvent,
    QResizeEvent,
    QPen,
    QColor,
    QFont,
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
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.textToDraw = ""

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)

        if self.textToDraw:
            self.drawText(painter, self.previousPoint, self.textToDraw)

        elif self.drawing:
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

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if a0:
            if a0.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
                self.drawText(
                    self.getImagePainter(), self.previousPoint, self.textToDraw
                )
                self.textToDraw = ""
            elif a0.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
                self.textToDraw = (
                    self.textToDraw[:-1]
                    if a0.key() == Qt.Key.Key_Backspace
                    else self.textToDraw
                )
            elif a0.key() >= 32 and a0.key() <= 126:
                self.textToDraw += a0.text()

        return super().keyPressEvent(a0)

    def drawText(self, painter: QPainter, position: QPoint, text: str):
        painter.setFont(QFont("Arial", 16))
        painter.drawText(position, text)

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
