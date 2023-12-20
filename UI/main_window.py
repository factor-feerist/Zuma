from PyQt6.QtWidgets import QMainWindow
from UI.application_widget import ApplicationWidget


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("ZUMA")
        self.app_widget = ApplicationWidget(exit_func=lambda: self.close())
        self.setCentralWidget(self.app_widget)
        self.resize(640, 480)
        pass



    pass
