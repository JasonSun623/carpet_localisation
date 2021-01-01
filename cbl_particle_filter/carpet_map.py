"""carpet_map.
defines representation of carpet map
"""

from typing import Tuple, Dict
import numpy as np
import cv2


class CarpetMap:
    """
    Representation of carpet.
    Specifically the color patern of a carpet.
    The pattern is represented as a grid, which each grid cell filled by a single color
    Colors are enumerated as integers; it is expected there is a fixed number of carpet colors

    Coordinate mapping:
    The bottom left corner of the bottom left cell in the 2d grid array is taken as the origin (0,0)
    The height/width of each cell is given by `cell_size`, so the top right corner of the bottom
    left cell in the grid is at coords (cell_size, cell_size)

    A cell is defined as occupying the half open interval from
    [index*cell_size : index+1*cell_size)

    e.g. for the 3rd cell from the left (i=2) with a cell size of 0.4, the
    cell covers the x-range (in m):
    [0.8:1.2)
    """
    def __init__(self, grid: np.array, cell_size: float):
        """
        grid: 2d array of carpet colors (ints)
        cell_size: size (in meters) of carpet grid cells
        """
        self.grid = grid
        self.cell_size = cell_size

    def get_color_at_coords(self, coords: np.array) -> np.array:
        """
        lookup color (int) in map at given x,y coordinates (in meters)
        input coords are given as nx2 array (for n coordinates)
        output colors are given as nx1 array of ints.
        Input coordinates which lie outside the bounds of the map
        will have an associated output value of -1
        """
        colors = np.full((coords.shape[0]), -1)

        x_indices = np.floor(coords[:, 0] / self.cell_size).astype(np.int)
        y_indices = np.ceil(self.grid.shape[0] - 1 -
                            (coords[:, 1] / self.cell_size)).astype(np.int)

        # avoid indexing points which are out of bounds
        in_bounds = ((x_indices >= 0) & (x_indices < self.grid.shape[1]) &
                     (y_indices >= 0) & (y_indices < self.grid.shape[0]))
        colors[in_bounds] = self.grid[y_indices[in_bounds],
                                      x_indices[in_bounds]]

        return colors


def generate_random_map(shape: Tuple[int, int], cell_size,
                        n_colors: int) -> CarpetMap:
    """
    Generate a random map of the given size with the given number of colors
    """
    return CarpetMap(grid=np.random.randint(0, high=n_colors, size=shape),
                     cell_size=cell_size)


def save_map_as_png(carpet_map: CarpetMap, color_to_rgb_map: Dict,
                    filepath: str):
    """
    Save a given map as a .png image
    """

    # convert the map grid (2d array of enums) to a cv2 image
    # (3d array of bgr values)

    image = np.zeros((
        carpet_map.grid.shape[0],
        carpet_map.grid.shape[1],
        3,
    ))

    # there's probably a nicer way to iterate over the image..
    # the idea is to replace each enum with the corresponding
    # bgr values in the output image
    for i in range(carpet_map.grid.shape[0]):
        for j in range(carpet_map.grid.shape[1]):
            color_enum = carpet_map.grid[i, j]
            r, g, b = color_to_rgb_map[color_enum]
            image[i, j, :] = (b, g, r)

    # rather than write image with only one pixel per cell,
    # upsample to `upsample_factor` pixels per cell
    # this avoids interpolation issues in some image viewers
    # and in gazebo
    upsample_factor = 50
    image = cv2.resize(
        image,
        dsize=(
            image.shape[0] * upsample_factor,
            image.shape[1] * upsample_factor,
        ),
        interpolation=cv2.INTER_NEAREST,
    )

    cv2.imwrite(filepath, image)