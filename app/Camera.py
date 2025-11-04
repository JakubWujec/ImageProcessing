import cv2
import sys


class Camera:
    def __init__(self) -> None:
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("Error: Camera not accessible")
            sys.exit()

    def getFrame(self):
        ret, frame = self.camera.read()
        if ret:
            return frame
        return None

    def close(self):
        self.camera.release()
