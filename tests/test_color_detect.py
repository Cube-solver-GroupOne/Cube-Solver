import pytest
from cube_steps_3D.color_detect import *


def test_camera_status():
    cap = cv2.VideoCapture(0)
    actual = cv2.VideoCapture.isOpened(cap)
    expected = True
    assert actual == expected


def test_camera_status_two():
    cap = cv2.VideoCapture(1)
    actual = cv2.VideoCapture.isOpened(cap)
    expected = True
    assert actual == expected


def test_positions():
    cube = CaptureCube

    actual = cube._positions
    expected = {
        (0, 0): (220, 140),
        (0, 1): (320, 140),
        (0, 2): (420, 140),
        (1, 0): (220, 240),
        (1, 1): (320, 240),
        (1, 2): (420, 240),
        (2, 0): (220, 340),
        (2, 1): (320, 340),
        (2, 2): (420, 340)
    }
    assert actual == expected


def test_colors():
    cube = CaptureCube
    actual = cube._colors
    expected = ['w', 'y', 'r', 'g', 'o', 'b']
    assert actual == expected


def test_faces_change():
    cube = CaptureCube
    actual = cube._trans
    expected = {
        'F': 'L',
        'L': 'B',
        'B': 'R',
        'R': 'U',
        'U': 'D',
        'D': 'N'
    }
    assert actual == expected


def test_crossbound():
    cube = CaptureCube
    actual = cube._cor_map
    expected = {
        'w': 'y',
        'y': 'r',
        'r': 'g',
        'g': 'o',
        'o': 'b',
        'b': 'w',
        'n': 'w'
    }
    assert actual == expected


def test_end_video():
    cube = CaptureCube
    actual = cube._filename
    expected = 'frame.png'
    assert actual == expected


def test_translate_solve_excpition():
    obj = {'U': {(0, 0): 'r', (0, 1): 'r', (0, 2): 'w', (1, 0): 'o', (1, 1): 'r', (1, 2): 'o', (2, 0): 'o', (2, 1): 'y',
                 (2, 2): 'o'},
           'D': {(0, 0): 'y', (0, 1): 'o', (0, 2): 'r', (1, 0): 'r', (1, 1): 'o', (1, 2): 'r', (2, 0): 'r', (2, 1): 'y',
                 (2, 2): 'o'},
           'F': {(0, 0): 'b', (0, 1): 'b', (0, 2): 'b', (1, 0): 'g', (1, 1): 'g', (1, 2): 'g', (2, 0): 'g', (2, 1): 'b',
                 (2, 2): 'g'},
           'L': {(0, 0): 'y', (0, 1): 'w', (0, 2): 'w', (1, 0): 'r', (1, 1): 'w', (1, 2): 'o', (2, 0): 'y', (2, 1): 'y',
                 (2, 2): 'o'},
           'B': {(0, 0): 'b', (0, 1): 'g', (0, 2): 'g', (1, 0): 'b', (1, 1): 'b', (1, 2): 'b', (2, 0): 'g', (2, 1): 'g',
                 (2, 2): 'b'},
           'R': {(0, 0): 'y', (0, 1): 'y', (0, 2): 'r', (1, 0): 'w', (1, 1): 'y', (1, 2): 'y', (2, 0): 'w', (2, 1): 'w',
                 (2, 2): 'w'}}
    try:
        actual = translate_solve("obj")
        assert False
    except Exception:
        assert True


def test_tranlate_3d():
    obj = "U R2 U' F2 D' B2 R2 D B2 U'"
    actual = tranlate_3d(obj)
    expected = ['TOP', 'RIGHT', 'RIGHT', 'TOPS', 'FACE', 'FACE', 'BOTTOMS', 'BACK', 'BACK', 'RIGHT', 'RIGHT', 'BOTTOM',
                'BACK', 'BACK', 'TOPS']
    assert actual == expected


def test_kosimba_mirror():
    result = "U R2 U' F2 D' B2 R2 D B2 U'"
    actual = kosimba_mirror(result)
    expected = "U B2 D' R2 B2 D F2 U R2 U'"
    assert actual == expected
