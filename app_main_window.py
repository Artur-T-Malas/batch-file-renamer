from PyQt6.QtWidgets import QMainWindow

from app_layout import AppLayout
from renamer import Renamer


class AppMainWindow(QMainWindow):
    def __init__(
            self,
            renamer: Renamer
        ):
        super().__init__()

        self.setWindowTitle("Batch File Renamer")

        self.app = AppLayout(renamer)

        self.setCentralWidget(self.app)
