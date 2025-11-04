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
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QLabel
from cv2.typing import MatLike


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("Error: Camera not accessible")
            sys.exit()

        self.cameraDisplay = QLabel(self)
        self.setCentralWidget(self.cameraDisplay)

        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(20)

    def run(self):
        frame = self.getCameraFrame()
        frame = self.processFrame(frame)
        self.showFrame(frame)

    def getCameraFrame(self):
        ret, frame = self.camera.read()
        if ret:
            return frame
        return None

    def processFrame(self, frame) -> MatLike:
        return frame

    def showFrame(self, frame: MatLike):
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
        q_img = QImage(frame.data, width, height, bytes_per_line, imageFormat)
        self.cameraDisplay.setPixmap(QPixmap.fromImage(q_img))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
