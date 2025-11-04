from typing import Dict
from app import (
    Camera,
    Canvas,
    ImageFilter,
    GaussianBlurFilter,
    CannyFilter,
    SharpenFilter,
    PencilSketchFilter,
)
import cv2


class AppState:
    def __init__(self) -> None:
        self.imageFilters: Dict[str, ImageFilter] = {
            "Gaussian Blur": GaussianBlurFilter(),
            "Canny": CannyFilter(),
            "Sharpen": SharpenFilter(),
            "Pencil Sketch": PencilSketchFilter(),
        }

        self.colorSpaceConversions = {
            "RGB": cv2.COLOR_BGR2RGB,
            "HSV": cv2.COLOR_BGR2HSV,
            "GRAY": cv2.COLOR_BGR2GRAY,
        }
        self.__currentColorSpaceConversion = cv2.COLOR_BGR2RGB

    def setColorSpaceConversion(self, colorSpaceConversion: int):
        self.__currentColorSpaceConversion = colorSpaceConversion

    @property
    def colorSpaceConversion(self):
        return self.__currentColorSpaceConversion
