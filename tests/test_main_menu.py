import pytest
from main_menu import MenuMenu

def test_MenuMenu():
    menu = MenuMenu()
    actual = menu.window.fullscreen
    expected = True
    assert actual == expected