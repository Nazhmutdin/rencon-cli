from pathlib import Path
from typing import Sequence

from PIL import Image
from numpy import ndarray, asarray
import cv2


class OpenCVSevice:

    @staticmethod
    def image_to_array(image: Image) -> ndarray:
        return asarray(image)


    @staticmethod
    def read_image(image: str | Path, flag: int = None) -> ndarray:
        return cv2.imread(image, flags=flag)


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
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    def _threshold_image(self, grayscale_image: ndarray) -> ndarray:
        return cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    def _invert_image(self, thresholded_image: ndarray) -> ndarray:
        return cv2.bitwise_not(thresholded_image)


    def _dilate_image(self, inverted_image: ndarray) -> ndarray:
        return cv2.dilate(inverted_image, None, iterations=5)
    

    def find_contours(self, dilated_image: ndarray, image: ndarray):
        contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Below lines are added to show all contours
        # This is not needed, but it is useful for debugging
        image_with_all_contours = image.copy()
        cv2.drawContours(image_with_all_contours, contours, -1, (0, 255, 0), 3)

        return contours, hierarchy


    def filter_contours_and_leave_only_rectangles(self, contours, image: ndarray):
        rectangular_contours = []
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                rectangular_contours.append(approx)
        # Below lines are added to show all rectangular contours
        # This is not needed, but it is useful for debugging
        image_with_only_rectangular_contours = image.copy()
        cv2.drawContours(image_with_only_rectangular_contours, rectangular_contours, -1, (0, 255, 0), 3)

        return rectangular_contours


    def find_largest_contour_by_area(self, rectangular_contours, image: ndarray):
        max_area = 0
        contour_with_max_area = None
        for contour in rectangular_contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                contour_with_max_area = contour
        # Below lines are added to show the contour with max area
        # This is not needed, but it is useful for debugging
        image_with_contour_with_max_area = image.copy()
        cv2.drawContours(image_with_contour_with_max_area, [contour_with_max_area], -1, (0, 255, 0), 3)

        return contour_with_max_area
