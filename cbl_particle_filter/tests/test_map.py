from ..carpet_map import CarpetMap, generate_random_map, save_map_as_png
import numpy as np
import tempfile
import os


def make_test_map() -> CarpetMap:
    return CarpetMap(
        grid=np.array([
            [1, 9, 2],
            [8, 3, 7],
            [4, 6, 5],
        ]),
        cell_size=0.4,
    )


def test_init():
    carpet = make_test_map()
    assert isinstance(carpet, CarpetMap)


def test_get_color_at_coords():
    carpet = make_test_map()

    coords = np.array([
        # two points in the bottom left cell, near the origin:
        [0.0, 0.0],
        [0.3, 0.1],
        # a series of randomly chosen points:
        [0.5, 0.7],
        [0.3, 1.1],
        [0.9, 0.01],
        [0.8001, 0.80001],
        [0.5, 1.0],
        # following four coords test out of bounds points - should
        # return color = -1
        [-1, 0.1],
        [0.1, -4],
        [1.21, 0.1],
        [0.1, 1.21],
    ])

    expected_colors = np.array([
        4,
        4,
        3,
        1,
        5,
        2,
        9,
        -1,
        -1,
        -1,
        -1,
    ])

    np.testing.assert_array_equal(expected_colors,
                                  carpet.get_color_at_coords(coords))


def test_generate_random_map():
    shape = (10, 20)
    cell_size = 0.5
    n_colors = 4
    carpet = generate_random_map(shape, cell_size, n_colors)

    assert isinstance(carpet, CarpetMap)
    assert carpet.cell_size == cell_size
    assert carpet.grid.shape == shape
    assert len(np.unique(carpet.grid)) == n_colors

    # for debug visualisation set plot=True
    plot = False
    if plot:
        from ..visualisation import plot_map
        plot_map(carpet)


def test_save_map_as_png():
    shape = (40, 40)
    cell_size = 0.5
    n_colors = 4
    np.random.seed(123)
    carpet = generate_random_map(shape, cell_size, n_colors)

    with tempfile.TemporaryDirectory() as tmpdirname:
        outfile = f"{tmpdirname}/saved_map.png"

        # To save the generated map for viewing, can
        # override outfile here:
        outfile = '/tmp/saved_map.png'

        save_map_as_png(carpet,
                        color_to_rgb_map={
                            0: (80, 80, 80),
                            1: (51, 204, 255),
                            2: (241, 230, 218),
                            3: (0, 51, 204),
                        },
                        filepath=outfile)
        assert os.path.isfile(outfile)
