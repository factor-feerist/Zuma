from PyQt6.QtWidgets import QStackedWidget
from UI.widgets.level_choosing_window import LevelChoosingWindow
from UI.widgets.win_window import WinWindow
from UI.widgets.lose_window import LoseWindow
from UI.widgets.screen_saver import ScreenSaver
from UI.widgets.game_widget import GameWidget
import utils


class ApplicationWidget(QStackedWidget):
    def __init__(self, exit_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_window = GameWidget(lambda x: self.open_win_window() \
            if x else self.open_lose_window())
        self.addWidget(self.game_window)
        self.level_choosing_window = LevelChoosingWindow(utils.get_all_levels(),
                                                         self.open_game, lambda: exit_func())
        self.addWidget(self.level_choosing_window)
        self.win_window = WinWindow(self.open_level_choosing_window)
        self.addWidget(self.win_window)
        self.lose_window = LoseWindow(self.open_level_choosing_window)
        self.addWidget(self.lose_window)
        self.screen_saver = ScreenSaver(self.open_level_choosing_window)
        self.addWidget(self.screen_saver)

        self.open_screen_saver()
        pass

    def open_screen_saver(self):
        self.setCurrentWidget(self.screen_saver)
        pass

    def open_game(self, level):
        print(f'open game on level {level}')
        self.setCurrentWidget(self.game_window)
        self.game_window.run_game(level)
        pass

    def open_level_choosing_window(self):
        self.setCurrentWidget(self.level_choosing_window)
        pass

    def open_win_window(self):
        self.setCurrentWidget(self.win_window)
        pass

    def open_lose_window(self):
        self.setCurrentWidget(self.lose_window)
        pass

    pass

