from pathlib import Path

from PIL import Image
from numpy import ndarray, asarray
import cv2 as cv


class OpenCVSevice:

    @staticmethod
    def image_to_array(image: Image) -> ndarray:
        return asarray(image)
    
    
    @staticmethod
    def read_image(image: str | Path, flag: int = None) -> ndarray:
        return cv.imread(image, flags=flag)
    

    def read_table(self, img: ndarray) -> list[list[str | int | float]]:
        ...

    
    def crop_image(self, img: ndarray, **kwargs) -> ndarray:
        """
        :absolute_coordinates is [x1: int, x2: int, y1: int, y2: int]
        :related_coordinates is [x1: float, x2: float, y1: float, y2: float] where x1, x2, y1, y2 in between 0 and 1
        """
        if kwargs.get("absolute_coordinates"):
            return self._crop_image(img, *kwargs.get("absolute_coordinates"))
        
        if kwargs.get("related_coordinates"):
            return self._crop_image(
                img, 
                *self._to_absolute_coordinates(img, kwargs.get("related_coordinates"))
            )
        
        raise ValueError("Invalid coordinates")


    def _crop_image(self, img: ndarray, x1: int, x2: int, y1: int, y2: int) -> ndarray: ...


    def _to_absolute_coordinates(self, img: ndarray, related_coordinates: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
        y_axis, x_axis = img.shape[:2]
        
        return (
            int(x_axis * related_coordinates[0]),
            int(x_axis * related_coordinates[1]),
            int(y_axis * related_coordinates[2]),
            int(y_axis * related_coordinates[3])
        )

    
    def _convert_image_to_grayscale(self, img: ndarray) -> ndarray:
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


    def _threshold_image(self, grayscale_image: ndarray) -> ndarray:
        return cv.threshold(grayscale_image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]


    def _invert_image(self, thresholded_image: ndarray) -> ndarray:
        return cv.bitwise_not(thresholded_image)


    def _dilate_image(self, inverted_image: ndarray) -> ndarray:
        return cv.dilate(inverted_image, None, iterations=5)