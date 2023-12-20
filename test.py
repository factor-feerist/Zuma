import sys
from PyQt6.QtWidgets import QApplication
import utils
from UI.widgets.game_widget import GameWidget


app = QApplication([])
#window = MainWindow()
frog_widget = GameWidget(lambda x: print(f'game ended with {x}'))
frog_widget.run_game(utils.Levels.FIRST)
#window.show()
frog_widget.show()
sys.exit(app.exec())
