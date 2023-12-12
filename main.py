import sys
from PyQt6.QtWidgets import QApplication
from frog_widget import FrogWidget

app = QApplication([])
#window = MainWindow()
frog_widget = FrogWidget()
#window.show()
frog_widget.show()
sys.exit(app.exec())
