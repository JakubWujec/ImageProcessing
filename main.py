import sys

import cv2
import numpy as np
from PyQt6.QtCore import QPoint, QSize, Qt, QTimer
from PyQt6.QtGui import (
    QAction,
    QActionGroup,
    QCloseEvent,
    QIcon,
    QImage,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFrame,
    QLabel,
    QStackedLayout,
    QSizePolicy,
    QButtonGroup,
    QToolButton,
    QVBoxLayout,
    QHBoxLayout,
)
from cv2.typing import MatLike

from app import Camera, Canvas
from app.DrawingTool import CircleTool, LineTool, PenTool, RectangleTool, TextTool


class UserInterface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.camera = Camera()

        mainWidget = QFrame(self)
        mainLayout = QVBoxLayout(mainWidget)

        layersWidget = QFrame(self)
        stacked_layout = QStackedLayout(layersWidget)
        stacked_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.cameraLayer = QLabel(self)
        self.cameraLayer.setScaledContents(True)

        self.canvasLayer = Canvas()

        stacked_layout.addWidget(self.canvasLayer)
        stacked_layout.addWidget(self.cameraLayer)

        toolbox = self.buildToolBox()

        mainLayout.addWidget(layersWidget)
        mainLayout.addWidget(toolbox)
        self.setCentralWidget(mainWidget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(20)

    def run(self):
        frame = self.camera.getFrame()
        if frame is not None:
            frame = self.processFrame(frame)
            image = self.frame_to_QImage(frame)
            self.cameraLayer.setPixmap(QPixmap.fromImage(image))
        self.canvasLayer.update()

    def processFrame(self, frame) -> MatLike:
        return frame

    def frame_to_QImage(self, frame: MatLike) -> QImage:
        height, width = frame.shape[:2]
        channel = frame.shape[2] if len(frame.shape) == 3 else 1
        if channel == 3:  # RGB
            bytes_per_line = 3 * width
            imageFormat = QImage.Format.Format_RGB888
        elif channel == 1:  # Grayscale
            bytes_per_line = width
            imageFormat = QImage.Format.Format_Grayscale8
        else:
            raise ValueError("Unsupported number of channels.")
        return QImage(frame.data, width, height, bytes_per_line, imageFormat)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.camera.close()

    def buildToolBox(self):
        widget = QWidget()
        widgetLayout = QHBoxLayout(widget)

        drawingToolsButtonGroup = QButtonGroup(self)

        tools = [
            {
                "icon": "assets/feather/rect.svg",
                "action": lambda: self.canvasLayer.setTool(RectangleTool()),
            },
            {
                "icon": "assets/feather/circle.svg",
                "action": lambda: self.canvasLayer.setTool(CircleTool()),
            },
            {
                "icon": "assets/feather/line.svg",
                "action": lambda: self.canvasLayer.setTool(LineTool()),
            },
            {
                "icon": "assets/feather/pen.svg",
                "action": lambda: self.canvasLayer.setTool(PenTool()),
            },
            {
                "icon": "assets/feather/type.svg",
                "action": lambda: self.canvasLayer.setTool(TextTool()),
            },
        ]

        for tool in tools:
            button = QToolButton()
            button.setIcon(QIcon(tool["icon"]))
            button.setIconSize(QSize(48, 48))
            button.setCheckable(True)
            button.clicked.connect(tool["action"])
            drawingToolsButtonGroup.addButton(button)
            widgetLayout.addWidget(button)

        clearButton = QToolButton()
        clearButton.setIcon(QIcon("assets/feather/clear.svg"))
        clearButton.setIconSize(QSize(48, 48))
        clearButton.clicked.connect(lambda: self.canvasLayer.clear())
        widgetLayout.addWidget(clearButton)

        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())
