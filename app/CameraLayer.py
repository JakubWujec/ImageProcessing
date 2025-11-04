import cv2
import sys
import numpy as np


class CameraLayer:
    def __init__(self) -> None:
        self.camera = cv2.VideoCapture(0)  # Use the default camera

        if not self.camera.isOpened():
            print("Error: Camera not accessible")
            sys.exit()

    def get_camera_frame(self):
        ret, frame = self.camera.read()
        frame = np.rot90(frame)
        return frame
