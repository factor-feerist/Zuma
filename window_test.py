import sys
from PyQt6.QtWidgets import QApplication
from UI.main_window import MainWindow


app = QApplication([])
widget = MainWindow()
widget.show()
sys.exit(app.exec())
