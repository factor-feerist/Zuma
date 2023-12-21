from src import src_helper
from pathlib import Path
from PyQt6.QtGui import QImage, QBrush, QPalette
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QUrl
from levels import level
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


def get_image_path(image_file_name):
    return str(Path(src_helper.get_path_to_me().parent, 'images', image_file_name))


def get_sound_path(sound_file_name):
    return str(Path(src_helper.get_path_to_me().parent, 'sound', sound_file_name))


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

    SECOND = level.make_second_level()


def get_all_levels():
    return [Levels.FIRST, Levels.SECOND]


class Sounds:
    SPIT = QUrl.fromLocalFile(get_sound_path('spit.mp3'))
    BALLS_DESTROYED = QUrl.fromLocalFile(get_sound_path('balls_destroyed.mp3'))
    SAD_TROMBONE = QUrl.fromLocalFile(get_sound_path('sad_trombone.mp3'))
    APPLAUSE = QUrl.fromLocalFile(get_sound_path('applause.mp3'))


player = QMediaPlayer()
aud = QAudioOutput()
player.setAudioOutput(aud)


def play_sound(sound):
    player.setSource(sound)
    player.setPosition(0)
    player.play()

