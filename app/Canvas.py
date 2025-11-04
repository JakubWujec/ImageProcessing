from PyQt6.QtCore import Qt, QPoint

from PyQt6.QtWidgets import (
    QFrame,
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
)

from app.DrawingTool import DrawingTool, PenTool, TextTool


class Canvas(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.image = QImage(self.size(), QImage.Format.Format_RGBA8888)
        self.startPoint = QPoint(50, 50)
        self.endPoint = QPoint()
        self.previousPoint = QPoint()
        self.drawing = False
        self.__currentTool: DrawingTool = PenTool()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)

        # draw preview
        if isinstance(self.__currentTool, TextTool):
            self.__currentTool.draw(painter, self.startPoint, self.endPoint)
        elif self.drawing:
            if not isinstance(self.__currentTool, PenTool):
                self.__currentTool.draw(painter, self.startPoint, self.endPoint)

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if a0:
            if a0.button() == Qt.MouseButton.LeftButton:
                self.startPoint = a0.position().toPoint()
                self.endPoint = self.startPoint
                self.previousPoint = self.startPoint
                self.drawing = True

            if a0.button() == Qt.MouseButton.RightButton:
                self.clear()
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if a0 and self.drawing:
            self.endPoint = a0.position().toPoint()
            self.update()

            if isinstance(self.__currentTool, PenTool):
                self.__currentTool.draw(
                    self.getImagePainter(), self.previousPoint, self.endPoint
                )

            self.previousPoint = self.endPoint

        return super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QMouseEvent | None):
        if a0 and a0.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.endPoint = a0.position().toPoint()
            self.drawing = False

            if not isinstance(self.__currentTool, PenTool) and not isinstance(
                self.__currentTool, TextTool
            ):
                self.drawWithCurrentTool()

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if isinstance(self.__currentTool, TextTool):
            if a0:
                if a0.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
                    self.drawWithCurrentTool()
                    self.__currentTool.textToDraw = ""
                elif a0.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
                    self.__currentTool.textToDraw = (
                        self.__currentTool.textToDraw[:-1]
                        if a0.key() == Qt.Key.Key_Backspace
                        else self.__currentTool.textToDraw
                    )

                elif a0.key() >= 32 and a0.key() <= 126:
                    self.__currentTool.textToDraw += a0.text()

        return super().keyPressEvent(a0)

    def getImagePainter(self):
        return QPainter(self.image)

    def drawWithCurrentTool(self):
        self.__currentTool.draw(self.getImagePainter(), self.startPoint, self.endPoint)

    def clear(self):
        self.image.fill(Qt.GlobalColor.transparent)

    def setTool(self, drawingTool: DrawingTool):
        self.__currentTool = drawingTool
        if isinstance(self.__currentTool, TextTool):
            self.__currentTool.textToDraw = ""

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.image = QImage(self.size(), QImage.Format.Format_RGBA8888)
        self.image.fill(Qt.GlobalColor.transparent)
        super().resizeEvent(a0)
