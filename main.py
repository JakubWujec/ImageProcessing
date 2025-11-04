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
)
from cv2.typing import MatLike

from app import Camera


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.camera = Camera()

        centralWidget = QWidget(self)
        stacked_layout = QStackedLayout(centralWidget)
        stacked_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.cameraDisplay = QLabel(self)
        stacked_layout.addWidget(self.cameraDisplay)

        self.setCentralWidget(centralWidget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(20)

    def run(self):
        frame = self.camera.getFrame()
        frame = self.processFrame(frame)
        image = self.frame_to_QImage(frame)
        self.cameraDisplay.setPixmap(QPixmap.fromImage(image))

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
