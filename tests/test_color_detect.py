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
    expected = False
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
