import sys
from PyQt6.QtWidgets import QApplication
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QVector2D
from balls import Ball, BallRepresentation, RollingBall, FlyingBall

from route import RouteLine, ComplexRoute
from PyQt6.QtGui import QImage
from frog import Frog

from UI.widgets.level_choosing_window import LevelChoosingWindow
from UI.main_window import MainWindow
from UI.application_widget import ApplicationWidget

app = QApplication([])
widget = MainWindow()
widget.show()
sys.exit(app.exec())
