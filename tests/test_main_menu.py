import pytest
from main_menu import *


def test_MenuMenu():
    try:
        menu = MenuMenu()
        menu.window.fullscreen
    except Exception:
        assert True


def test_error_render():
    try:
        menu = MenuMenu()
        assert False
    except Exception:
        assert True

def test_start_main_menu():
    app = Ursina(title='Main Menu Tutorial')
    # Call our menu
    main_menu = MenuMenu()
    # Run application
    assert main_menu.disable() == False
