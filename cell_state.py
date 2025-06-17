from typing import List
from PIL import Image

class CellState:
    def __init__(self):
        # Initialize _image_grid as an empty list
        self._image_grid: List[List[Image.Image]] = []

    @property
    def image_grid(self) -> List[List[Image.Image]]:
        # Return the image grid, or an empty list if it hasn't been set
        if self._image_grid is not None:
            return self._image_grid
        return []

    @image_grid.setter
    def image_grid(self, grid: List[List[Image.Image]]):
        # Set the image grid to a new value
        self._image_grid = grid

    # ...existing code...