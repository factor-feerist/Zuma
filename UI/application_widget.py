from PyQt6.QtWidgets import QStackedWidget
from UI.widgets.level_choosing_window import LevelChoosingWindow


class ApplicationWidget(QStackedWidget):
    def __init__(self, exit_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_window = None
        self.level_choosing_window = LevelChoosingWindow([1, 2, 3, 4], lambda: exit_func())
        self.win_window = None
        self.lose_window = None
        self.addWidget(self.level_choosing_window)
        self.setCurrentWidget(self.level_choosing_window)


        pass


    pass

