from abc import abstractmethod
import cv2
import numpy as np
from cv2.typing import MatLike


class ImageFilter:
    def __init__(self) -> None:
        self.__isOn: bool = False

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def isOn(self):
        return self.__isOn

    def toggle(self):
        if self.__isOn:
            self.__isOn = False
        else:
            self.__isOn = True

    def apply(self, frame: MatLike):
        raise NotImplementedError()


class GaussianBlurFilter(ImageFilter):
    def __init__(self, kernel_size=(5, 5)):
        super().__init__()
        self.kernel_size = kernel_size

    def apply(self, frame):
        return cv2.GaussianBlur(frame, self.kernel_size, 0)


class CannyFilter(ImageFilter):
    def __init__(self, lower_threshold=100, upper_threshold=200):
        super().__init__()
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def apply(self, frame):
        return cv2.Canny(frame, self.lower_threshold, self.upper_threshold)


class SharpenFilter(ImageFilter):
    def __init__(self):
        super().__init__()

    def apply(self, frame):
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        frame = cv2.filter2D(frame, -1, kernel)
        return frame


class PencilSketchFilter(ImageFilter):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, frame):
        if frame.shape == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(frame, (21, 21), 0)
        final_image = cv2.divide(frame, blurred_image, scale=256)
        ret, mask = cv2.threshold(final_image, 70, 255, cv2.THRESH_BINARY)
        sketched_image = cv2.bitwise_and(mask, final_image)
        return sketched_image
