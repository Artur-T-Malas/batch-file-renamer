from PyQt6.QtWidgets import QMainWindow

from .app_layout import AppLayout


class AppMainWindow(QMainWindow):
    def __init__(
            self,
            app_layout: AppLayout,
            window_title: str
        ):
        super().__init__()

        self.setWindowTitle(window_title)
        self.setCentralWidget(app_layout)
