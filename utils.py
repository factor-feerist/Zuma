from src import src_helper
from pathlib import Path
from PyQt6.QtGui import QImage, QBrush, QPalette
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from levels import level


def get_image_path(image_file_name):
    return str(Path(src_helper.get_path_to_me().parent, 'images', image_file_name))


def set_image_to_background(widget: QWidget, image):
    def set_background():
        img = image.scaled(widget.size(),
                           Qt.AspectRatioMode.IgnoreAspectRatio)
        brush = QBrush(img)
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        widget.setPalette(palette)
        pass
    widget.setAutoFillBackground(True)
    set_background()
    widget.resizeEvent = lambda a: set_background()
    pass


class Images:
    FROG_WITH_HAT = QImage(get_image_path('frog_in_hat.jpeg'))

    FROG_WITH_GUN = QImage(get_image_path('frog_with_gun.jpg'))

    SCARED_SNAKE = QImage(get_image_path('scared_snake.jpg'))


class Levels:
    FIRST = level.make_first_level()


def get_all_levels():
    return [Levels.FIRST]
