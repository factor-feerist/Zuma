from PyQt6.QtWidgets import QStackedWidget
from UI.widgets.level_choosing_window import LevelChoosingWindow
from UI.widgets.win_window import WinWindow
from UI.widgets.game_window_mock import GameWindowMock
from UI.widgets.lose_window import LoseWindow
from UI.widgets.screen_saver import ScreenSaver


class ApplicationWidget(QStackedWidget):
    def __init__(self, exit_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_window = GameWindowMock(on_win=self.open_win_window,
                                          on_lose=self.open_lose_window)
        self.addWidget(self.game_window)
        self.level_choosing_window = LevelChoosingWindow([1, 2, 3, 4], self.open_game, lambda: exit_func())
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
        # do something
        print(f'open game on level {level}')
        self.setCurrentWidget(self.game_window)
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

